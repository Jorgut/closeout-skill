---
description: Reconcile project docs, rules, memory, and workspace state
---

Use the `closeout` skill to perform knowledge and governance closeout for the
current project.

Treat `$ARGUMENTS` as additional scope or constraints. Preserve the skill's
permission boundaries: report destructive cleanup candidates first and do not
delete, rename, or modify out-of-scope resources without explicit confirmation.
