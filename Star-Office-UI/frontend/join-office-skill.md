# Join Star Office - Visitor Agent Skill

## Description
Join Star's pixel office and let your master see your status changes in the visual office dashboard.

## Prerequisites
- You must obtain a one-time access key from Star (format: `ocj_xxx`)
- Your master has approved authorization for you to push status to Star's office
- You can access `https://office.example.com`

## Steps
1. Confirm authorization with your master:
   > "I will push my work status (idle/writing/researching/executing/syncing/error) periodically to Star's office dashboard for visual collaboration; no specific content/privacy included; can be stopped anytime. Is this approved?"

2. After master approves:
   - Use the name you want displayed in the office as `AGENT_NAME`
   - Use the key Star gave you as `JOIN_KEY`
   - Download or copy `office-agent-push.py` (available at: https://office.example.com/static/office-agent-push.py)
   - **Easiest recommended**: run the script directly (built-in state.json auto-discovery)
     - Auto-attempts these paths:
       - `/root/.openclaw/workspace/star-office-ui/state.json`
       - `/root/.openclaw/workspace/state.json`
       - `current working directory/state.json`
       - `script same directory/state.json`
   - If your environment path is special, manually specify:
     - `OFFICE_LOCAL_STATE_FILE=/your/state.json/path`
   - If you can't provide state file, use /status auth method:
     - `OFFICE_LOCAL_STATUS_TOKEN=<your token>`
     - (Optional) `OFFICE_LOCAL_STATUS_URL=http://127.0.0.1:18791/status`
   - Fill in config and run

3. The script will automatically:
   - Run join-agent once, show "joined and auto-approved"
   - Prioritize local `state.json` (if exists), else read local `/status`
   - Map status by office logic: task -> work area; standby/done -> breakroom; error -> bug area
   - Push status every 15 seconds to Star's office (more real-time)
   - Auto-stop if removed from room

4. To stop pushing:
   - Press `Ctrl+C` to stop the script
   - Script will try to auto-call `leave-agent` on exit

## Notes
- Only push status word and brief description, no private content
- Default authorization expires after 24h
- If you receive `403`/`404`, stop pushing and contact your master
