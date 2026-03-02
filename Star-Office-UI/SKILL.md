---
name: star-office-ui
description: Star Office UI One-Click Skill: helps users quickly deploy a pixel office dashboard, supporting multi-agent joins, status visualization, mobile view and public access.
---

# Star Office UI Skill

This Skill is for OpenClaw (Lobster) users who want to quickly help their master set up a "pixel office dashboard":
- Goal: your master sees the results with minimal questions
- Follow the steps below to get it running and accessible to the public

---

## 0. Explain in One Sentence

You can tell your master:
> This is a multi-person collaboration pixel office dashboard where your AI assistants move to different positions based on status, and you can see yesterday's work notes!

---

## 1. 30-Second One-Click Launch (Recommended: do this first)

Run on your machine (in order):

```bash
# 1) Clone repository
git clone https://github.com/ringhyacinth/Star-Office-UI.git
cd Star-Office-UI

# 2) Install dependencies
python3 -m pip install -r backend/requirements.txt

# 3) Prepare state file (first time)
cp state.sample.json state.json

# 4) Start backend
cd backend
python3 app.py
```

Then tell your master:
> Great! Open http://127.0.0.1:18791 to see the pixel office!

---

## 2. Help Master Experience Status Changes

Run in the project root:

```bash
# Working → go to the desk
python3 set_state.py writing "Helping you organize documents"

# Syncing
python3 set_state.py syncing "Syncing progress"

# Error → go to bug area
python3 set_state.py error "Found a problem, investigating"

# Standby → back to breakroom
python3 set_state.py idle "Standing by, ready to serve"
```

---

## 3. 帮主人公网化（对外访问）

### 推荐方式：Cloudflare Tunnel（最快）

如果你这台机器有 `cloudflared`，直接跑：

```bash
cloudflared tunnel --url http://127.0.0.1:18791
```

会得到一个 `https://xxx.trycloudflare.com` 链接，发给主人即可。

如果没有 `cloudflared`，也可以用你自己熟悉的公网方案（Nginx/Caddy 反向代理 / 自有域名 / 其他隧道等）。

---

## 4. 邀请其他龙虾加入（可选）

如果有其他 OpenClaw 想加入你主人的办公室：

### 步骤 A：告诉其他龙虾用 office-agent-push.py

你可以让其他龙虾：
1) 下载 `office-agent-push.py`（可以直接从你这个仓库拿）
2) 让它调用 `join-agent` + 周期 `agent-push`
3) 你主人那边就能看到它进办公室了

### 步骤 B：join key 说明

- 仓库里默认有 `join-keys.json`（`ocj_starteam01` ~ `ocj_starteam08`）
- 同一个 key 最多 3 人同时在线
- 你也可以帮主人新建自己的 key

---

## 5. 昨日小记（可选）

如果你主人想看到“昨日小记”：
- 在仓库上级目录放一个 `memory/YYYY-MM-DD.md`
- 后端会自动读取昨天（或最近可用）的记录，做基础脱敏后展示

---

## 6. 常见问题（主人可能问你的）

### Q1：“为什么角色选了宝石海星？”
> 宝石海星是宝可梦的 IP，不是原创的；选它是因为和作者名字“海辛”在中文里有谐音趣味，这是一个非商用的粉丝创作，仅供学习演示。

### Q2：“我可以商用吗？”
> 代码玩法可以基于 MIT 用，但美术资产（包括角色/场景）禁止商用；如果你要商用，请务必换成你自己的原创美术资产。

### Q3：“其他龙虾怎么加入？”
> 用 join key 加入，然后持续推送状态就行；仓库里有 `office-agent-push.py` 可以给其他龙虾用。

---

## 7. 给你的提示

- 尽量帮主人把“启动步骤”做完，让主人只负责“看”和“体验”
- 如果主人要对外访问，优先用 Cloudflare Tunnel（最快最方便）
- 如果主人要改状态，你可以帮他调用 `set_state.py`，不用让他自己敲命令
- 注意不要暴露你主人的内网地址或私有信息
