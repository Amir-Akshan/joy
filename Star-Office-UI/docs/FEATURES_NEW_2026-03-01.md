# Star Office UI — New Features (This Phase)

## 1. Multi-Lobster Visitor System
- Support multiple remote OpenClaw instances joining the same office simultaneously.
- Visitors support independent avatar, name, status, area, and speech bubble.
- Support dynamic online/offline and real-time refresh.

## 2. Join Key Mechanism Upgrade
- Upgraded from "one-time key" to "fixed reusable key".
- Default keys: `ocj_starteam01` ~ `ocj_starteam08`.
- Preserved security controls: each key has `maxConcurrent` limit (default 3).

## 3. Concurrency Control (Race Condition Fixed)
- Fixed race condition in concurrent join operations.
- 4th concurrent join with same key correctly rejected (HTTP 429).

## 4. Visitor Status Mapping & Area Rendering
- `idle -> breakroom`
- `writing/researching/executing/syncing -> writing`
- `error -> error`
- Visitor speech bubble text syncs with status, no misalignment.

## 5. Visitor Animation & Resource Optimization
- Visitors upgraded from static image to animation sprite (pixel art).
- `guest_anim_1~6` provided in webp format, reduced load size.

## 6. Name & Speech Bubble Display Optimization
- Non-demo visitor names and speech balloon positions moved up, avoiding character occlusion.
- Speech bubble anchor changed to name-based positioning, ensuring "bubble above name".

## 7. Mobile Display
- Page can be directly accessed and displayed on mobile devices.
- Layout adapted for basic mobile display, meeting demo scenarios.

## 8. Remote Push Script Integration Improvements
- Support reading status from state file and pushing to office.
- Added status source diagnostic logging (for locating "why always idle").
- Fixed AGENT_NAME environment variable override timing issue.
