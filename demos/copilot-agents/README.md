# Copilot Agents Demo

Use the following 3 files to setup your Copilot Agents demo. 
Paste the ISSUE.md file into a new issue in that repository. 

## What this demo shows
- Assign an issue to Copilot to start an agent task
- Monitor progress in AgentHQ
- Re-steer mid-session with a new requirement
- Review the resulting PR like a teammate’s work

## Demo files
- `ISSUE.md` contains the exact issue text to copy/paste into GitHub
- `STEER.md` contains the mid-session requirement change to paste while the agent is working

## Quick demo steps
1. Create a new GitHub Issue by copying the Title and Body from `ISSUE.md`
2. Assign the issue to Copilot to start the agent task
3. Open AgentHQ to monitor progress
4. Paste `STEER.md` into the agent session to re-steer the work
5. Review the PR diff for clarity, completeness, and constraints.
6. Verify the PR edited the README.md file by adding priority levels plus the steered examples. 

---

## Ticket Triage Policy (Current)

We currently triage support tickets using Severity only.

### Severity levels
- Low means minor annoyance with an easy workaround
- Medium means a meaningful user impact but workarounds exist
- High means blocks key workflows or causes data loss

### Priority levels

- **P0** (Critical): Service down, data loss, or security breach. Immediate action required.
- **P1** (High): Major feature broken, significant user impact, no workaround. Address within hours.
- **P2** (Medium): Important issue with workaround available. Address within days.
- **P3** (Low): Minor issue, cosmetic bug, or enhancement request. Address when capacity allows.

### Severity to Priority mapping

| Severity | Default Priority | Notes |
|----------|-----------------|-------|
| High | P0 or P1 | P0 if service impact, P1 if feature impact |
| Medium | P2 | Can escalate to P1 if affecting many users |
| Low | P3 | Can escalate if accumulating user complaints |

### How to triage in 60 seconds

1. **Identify impact**: How many users affected? Is service down?
2. **Check severity**: Low, Medium, or High based on impact and workarounds
3. **Assign priority**: Use the Severity to Priority mapping above
4. **Tag & assign**: Add priority label and assign to appropriate team/person
5. **Set expectations**: Comment with expected timeline based on priority

### Current rules
- Triage happens daily
- High severity should be addressed first
- Priority labels guide the order of work within each severity level
