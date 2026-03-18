# APEX Userbot - Update Module
# git fetch ile yenilik yoxla, changelog goster, .update now ile yenile

import os
import asyncio
import subprocess
from userbot import LOGS, CMD_HELP, UPSTREAM_REPO_URL, APEX_VERSION
from userbot.events import register
from userbot.cmdhelp import CmdHelp

HF_TOKEN = os.environ.get("HF_TOKEN", None)
HF_SPACE_ID = os.environ.get("HF_SPACE_ID", None)


def _run_git(cmd):
    """Git əmrini işlət, nəticəni qaytar."""
    try:
        result = subprocess.run(
            cmd, shell=True,
            capture_output=True, text=True, timeout=30
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Git əmri vaxt aşımına uğradı (30 san)"
    except Exception as e:
        return -1, "", str(e)


def _ensure_remote():
    """upstream remote-un mövcud olduğunu təmin et."""
    code, out, _ = _run_git("git remote")
    if "upstream" not in out.split():
        _run_git(f"git remote add upstream {UPSTREAM_REPO_URL}")


def _get_changelog():
    """GitHub-dan yenilikləri yoxla və changelog qaytar."""
    _ensure_remote()

    # Remote-u fetch et
    code, _, err = _run_git("git fetch upstream main")
    if code != 0:
        # upstream yoxdursa origin-dən çək
        code, _, err = _run_git("git fetch origin main")
        if code != 0:
            return None, f"Git fetch xətası: {err}"
        remote_branch = "origin/main"
    else:
        remote_branch = "upstream/main"

    # Yeni commitlər varmı?
    code, log_out, _ = _run_git(
        f'git log HEAD..{remote_branch} --oneline --no-merges'
    )
    if code != 0 or not log_out:
        return [], None  # Yenilik yoxdur

    commits = log_out.strip().split("\n")

    # Dəyişən fayllar
    code, files_out, _ = _run_git(
        f'git diff --stat HEAD..{remote_branch}'
    )

    return {
        "commits": commits,
        "files": files_out,
        "remote": remote_branch,
        "count": len(commits)
    }, None


# ═══════════════════════════════════════
# .update — yenilikləri yoxla
# ═══════════════════════════════════════

@register(outgoing=True, pattern=r"^\.update(?: |$)(.*)")
async def update_bot(event):
    args = event.pattern_match.group(1).strip().lower()

    # ─── .update (boş) — yenilikləri yoxla ───
    if not args:
        await event.edit("`🔍 Yenilikler yoxlanılır...`")

        changelog, error = _get_changelog()

        if error:
            return await event.edit(f"❌ **Yenilik yoxlanarkən xəta:**\n`{error}`")

        if not changelog:
            return await event.edit(
                f"✅ **Bot ən son versiyadadır!**\n\n"
                f"📌 **Versiya:** `{APEX_VERSION}`\n"
                f"🔗 **Repo:** `{UPSTREAM_REPO_URL}`"
            )

        # Yenilikləri göstər
        text = (
            f"🆕 **{changelog['count']} yeni yenilik tapıldı!**\n\n"
            f"**📋 Dəyişikliklər:**\n"
        )
        for commit in changelog['commits'][:15]:
            hash_id = commit[:7]
            msg = commit[8:] if len(commit) > 8 else commit
            text += f"  `{hash_id}` — {msg}\n"

        if changelog['count'] > 15:
            text += f"  ... və daha {changelog['count'] - 15} commit\n"

        if changelog['files']:
            text += f"\n**📁 Dəyişən fayllar:**\n`{changelog['files'][-200:]}`\n"

        text += (
            f"\n**Yeniləmək üçün:**\n"
            f"`.update now` — yenilikləri yüklə və botu restart et"
        )
        return await event.edit(text)

    # ─── .update now — yeniləmə tətbiq et ───
    if args in ("now", "install", "yes"):
        await event.edit("`⬇️ Yenilikler yüklənir...`")

        # DB backup al
        try:
            from userbot.modules.db_backup import backup_db
            backup_ok = await backup_db(event.client)
            if backup_ok:
                await event.edit("`✅ DB backup alındı.\n⬇️ Yenilikler yüklənir...`")
        except Exception:
            pass

        # HuggingFace Space restart (əgər HF-dədirsə)
        if HF_TOKEN and HF_SPACE_ID:
            try:
                from huggingface_hub import HfApi
                api = HfApi(token=HF_TOKEN)
                api.restart_space(HF_SPACE_ID)

                return await event.edit(
                    "✅ **Yeniləmə başladı!**\n\n"
                    "🔄 HF Space restart edilir...\n"
                    "⬇️ Git pull ilə son kod çəkiləcək.\n"
                    "💾 DB backup-dan bərpa olunacaq.\n\n"
                    "⏱ Bot **2-3 dəqiqə** ərzində yenidən aktivləşəcək."
                )
            except Exception as e:
                LOGS.error(f"HF Space restart xətası: {e}")
                await event.edit(
                    f"`⚠️ HF Space restart xətası: {e}`\n"
                    "`Git pull ilə birbaşa yeniləməyə çalışıram...`"
                )

        # Birbaşa git pull (local və ya HF xətası halında)
        _ensure_remote()
        code, out, err = _run_git("git pull upstream main --rebase")
        if code != 0:
            code, out, err = _run_git("git pull origin main --rebase")

        if code != 0:
            # Force pull
            code, out, err = _run_git("git fetch origin main && git reset --hard origin/main")

        if code != 0:
            return await event.edit(
                f"❌ **Git pull xətası:**\n`{err[:300]}`\n\n"
                f"Manual yeniləmə: HF Space-i restart edin."
            )

        # Restart
        await event.edit(
            "✅ **Yenilikler yükləndi!**\n\n"
            f"```{out[:300]}```\n\n"
            "🔄 Bot yenidən başladılır..."
        )

        import asyncio as _asyncio
        await _asyncio.sleep(1)

        # HF Space-dədirsə os._exit(0)
        if os.environ.get("SPACE_ID") or os.environ.get("HF_SPACE_ID"):
            os._exit(0)
        else:
            # Local-da execl ilə restart
            import sys
            from os import execl as _execl
            try:
                await event.client.disconnect()
            except Exception:
                pass
            _execl(sys.executable, sys.executable, *sys.argv)

    else:
        return await event.edit(
            f"❓ **Tanınmayan parametr:** `{args}`\n\n"
            f"`.update` — yenilikləri yoxla\n"
            f"`.update now` — yenilikləri yüklə və restart et"
        )


CmdHelp('update').add_command(
    'update', None,
    'GitHub-dan yenilikləri yoxla. Nə dəyişdiyini göstərir.',
    'update'
).add_command(
    'update now', None,
    'Yenilikləri yüklə və botu restart et. HF Space-də avtomatik restart edir.',
    'update now'
).add_info(
    'Bot yeniləmə sistemi. GitHub-dan son dəyişiklikləri yoxlayır, changelog göstərir və yeniləyir.'
).add()
