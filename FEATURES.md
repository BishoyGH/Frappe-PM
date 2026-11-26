# Frappe PM: Feature List (Draft for Approval)

Repo state: `BishoyGH/Frappe-PM` is empty (no commits, no branches), so this is a greenfield Frappe app.

Tiers: **MVP** = ships in the first release of the single PR; **P2** = included in the PR if time allows, else fast follow; **P3** = later/optional.

Approach: native Frappe wherever possible (DocTypes, Workflow, Kanban/Gantt/Calendar views, Script Reports, Dashboard Charts, Notification, Assignment Rule, Web Form/Portal, REST API).

Total features: **382** (MVP 148, P2 118, P3 116)


## 1. Projects

| # | Feature | Tier |
|---|---|---|
| 1 | Project DocType with status, priority, dates, owner, department | MVP |
| 2 | Project templates with prebuilt task trees | MVP |
| 3 | Project types (internal, client, R&D, support) | MVP |
| 4 | Project health indicator (RAG status, auto-computed) | MVP |
| 5 | Project hierarchy: programs and portfolios (parent/child) | P2 |
| 6 | Project members child table with project roles | MVP |
| 7 | Project stakeholders register | P2 |
| 8 | Project milestones DocType with due dates and completion | MVP |
| 9 | Project phases/stages | P2 |
| 10 | Project cloning/duplication with date shifting | P2 |
| 11 | Project archive and restore | MVP |
| 12 | Project custom fields via Frappe Custom Field support | MVP |
| 13 | Project tags and categories | MVP |
| 14 | Project favourites/pinning for each user | P2 |
| 15 | Project status updates (periodic posts with RAG) | P2 |
| 16 | Project charter/brief document section | P2 |
| 17 | Project risk register (probability, impact, mitigation) | P2 |
| 18 | Project issue log | P2 |
| 19 | Project assumptions and dependencies log | P3 |
| 20 | Project change requests with approval workflow | P2 |
| 21 | Project closure checklist and lessons learned | P3 |
| 22 | Project baseline snapshots for variance tracking | P3 |
| 23 | Project cost center linkage | P3 |
| 24 | Project customer linkage (CRM-style) | P2 |
| 25 | Project overview dashboard page | MVP |

## 2. Tasks and work items

| # | Feature | Tier |
|---|---|---|
| 26 | Task DocType with status, priority, assignee, dates, estimate | MVP |
| 27 | Subtasks (nested tree view via is_group) | MVP |
| 28 | Task types (task, bug, story, epic, milestone, chore) | MVP |
| 29 | Custom task statuses per project | P2 |
| 30 | Task priority levels with colors | MVP |
| 31 | Multiple assignees per task (Frappe assignments) | MVP |
| 32 | Task watchers/followers | MVP |
| 33 | Task descriptions with rich text editor | MVP |
| 34 | Task checklists (child table items) | MVP |
| 35 | Task attachments (native Frappe file attach) | MVP |
| 36 | Task comments with @mentions | MVP |
| 37 | Task activity timeline (version log) | MVP |
| 38 | Task dependencies (finish-to-start, SS, FF, SF) | MVP |
| 39 | Task blocking/blocked-by indicators | P2 |
| 40 | Task labels/tags | MVP |
| 41 | Task story points | MVP |
| 42 | Task time estimates (hours) vs actuals | MVP |
| 43 | Task due date, start date, and overdue flag | MVP |
| 44 | Recurring tasks (daily/weekly/monthly/custom) | P2 |
| 45 | Task templates | P2 |
| 46 | Task cloning | MVP |
| 47 | Task move between projects | P2 |
| 48 | Bulk edit tasks (list view) | MVP |
| 49 | Bulk assign/status change | MVP |
| 50 | Task import from CSV/Excel (Data Import) | MVP |
| 51 | Task export (CSV/Excel/PDF) | MVP |
| 52 | Task linking (relates to, duplicates, causes) | P2 |
| 53 | Task progress percent (manual or computed from subtasks) | MVP |
| 54 | Auto-close parent when all subtasks done | P2 |
| 55 | Task reminders | P2 |
| 56 | Task custom fields | MVP |
| 57 | Task print format | P3 |
| 58 | Task quick-add from anywhere (keyboard shortcut) | P2 |
| 59 | My Tasks personal workspace page | MVP |
| 60 | Task email-to-create (inbound email rule) | P3 |
| 61 | Task voting/watch counts | P3 |
| 62 | Task acceptance criteria field | P2 |
| 63 | Task reopen with reason | P2 |
| 64 | Task archiving | P3 |
| 65 | Task rank/ordering within backlog (drag reorder) | P2 |

## 3. Agile: backlog, sprints, boards

| # | Feature | Tier |
|---|---|---|
| 66 | Product backlog list with prioritization | MVP |
| 67 | Epic DocType with child stories rollup | P2 |
| 68 | Sprint DocType (goal, start, end, capacity) | MVP |
| 69 | Sprint planning view (drag from backlog) | MVP |
| 70 | Sprint capacity planning per member | P2 |
| 71 | Sprint start/complete actions with carry-over | MVP |
| 72 | Sprint burndown chart | MVP |
| 73 | Sprint burnup chart | P2 |
| 74 | Velocity chart across sprints | P2 |
| 75 | Sprint report (completed, incomplete, added) | P2 |
| 76 | Sprint retrospective DocType (went well, improve, actions) | P3 |
| 77 | Kanban board per project (Frappe Kanban Board) | MVP |
| 78 | Custom Kanban columns mapped to statuses | MVP |
| 79 | Drag-and-drop card moves with status update | MVP |
| 80 | WIP limits per column | P2 |
| 81 | Swimlanes by assignee/epic/priority | P3 |
| 82 | Board filters and quick search | MVP |
| 83 | Card cover colors and badges | P3 |
| 84 | Scrum board (sprint-scoped) | MVP |
| 85 | Cumulative flow diagram | P3 |
| 86 | Cycle time and lead time reports | P3 |
| 87 | Definition of Done checklist | P3 |
| 88 | Release/version DocType (fix version) | P2 |
| 89 | Release notes generation | P3 |
| 90 | Story point estimation (planning poker session) | P3 |
| 91 | Backlog grooming flags | P3 |
| 92 | User story template with As-a/I-want/So-that fields | P2 |
| 93 | Bug tracking fields (severity, steps, environment) | MVP |
| 94 | Bug triage queue | P2 |
| 95 | Sprint auto-creation on schedule | P3 |

## 4. Views and visualization

| # | Feature | Tier |
|---|---|---|
| 96 | List view with saved filters | MVP |
| 97 | Report view with column picker | MVP |
| 98 | Calendar view of tasks and milestones | MVP |
| 99 | Gantt view (Frappe Gantt) with dependencies | MVP |
| 100 | Gantt drag to reschedule | P2 |
| 101 | Gantt critical path highlighting | P3 |
| 102 | Gantt baseline overlay | P3 |
| 103 | Timeline/roadmap view by epic and release | P2 |
| 104 | Tree view of project/task hierarchy | MVP |
| 105 | Group-by sidebar counts (assignee, status, tag) | MVP |
| 106 | Dashboard view with charts | MVP |
| 107 | Image/card gallery view | P3 |
| 108 | Workload view per member | P2 |
| 109 | Map view for field tasks (geolocation) | P3 |
| 110 | Table (spreadsheet-style) inline editing view | P2 |
| 111 | Saved view presets shareable across team | P2 |
| 112 | Dark mode (Frappe themes) | MVP |
| 113 | Customizable workspace shortcuts | MVP |
| 114 | Number cards on workspace (open tasks, overdue) | MVP |
| 115 | Mind-map view of task tree | P3 |

## 5. Time tracking

| # | Feature | Tier |
|---|---|---|
| 116 | Timesheet DocType with daily/weekly entries | MVP |
| 117 | Time log child table linked to task and project | MVP |
| 118 | Start/stop timer on task form | MVP |
| 119 | Manual time entry with validation | MVP |
| 120 | Billable vs non-billable hours | MVP |
| 121 | Activity types with billing/cost rates | MVP |
| 122 | Timesheet submit and approval workflow | MVP |
| 123 | Weekly timesheet grid UI | P2 |
| 124 | Overlapping time entry prevention | P2 |
| 125 | Timesheet reminders for missing logs | P2 |
| 126 | Time lock periods (no edits after close) | P3 |
| 127 | Time-by-project and time-by-user reports | MVP |
| 128 | Estimated vs actual hours variance report | MVP |
| 129 | Idle timer detection prompt | P3 |
| 130 | Time off / leave integration (HRMS optional) | P3 |
| 131 | Timesheet export for invoicing | P2 |
| 132 | Overtime flags and thresholds | P3 |
| 133 | Mobile-friendly timer widget | P2 |
| 134 | Time entry from calendar drag | P3 |
| 135 | Timesheet to sales invoice generation (ERPNext optional) | P3 |

## 6. Resource management

| # | Feature | Tier |
|---|---|---|
| 136 | Resource profile (skills, role, cost rate, capacity) | P2 |
| 137 | Skills master and proficiency levels | P2 |
| 138 | Resource allocation DocType (project, user, %, dates) | P2 |
| 139 | Resource capacity calendar | P2 |
| 140 | Over-allocation warnings | P2 |
| 141 | Resource availability finder by skill | P3 |
| 142 | Team DocType with members and lead | MVP |
| 143 | Utilization report (billable vs capacity) | P2 |
| 144 | Holiday list integration for working-day math | MVP |
| 145 | Working hours and weekends configuration | MVP |
| 146 | Resource forecasting heatmap | P3 |
| 147 | Resource requests/booking workflow | P3 |
| 148 | Equipment/asset allocation to projects | P3 |
| 149 | External contractor/vendor resources | P3 |
| 150 | Role-based rate cards | P2 |

## 7. Budget, cost, and finance

| # | Feature | Tier |
|---|---|---|
| 151 | Project budget DocType (by category) | P2 |
| 152 | Budget vs actual tracking | P2 |
| 153 | Cost from timesheets (labor cost) | P2 |
| 154 | Expense claims linked to project | P2 |
| 155 | Purchase/vendor cost linking (ERPNext optional) | P3 |
| 156 | Billing types (fixed price, T&M, milestone) | P2 |
| 157 | Milestone billing triggers | P3 |
| 158 | Invoice generation from billable time | P3 |
| 159 | Profitability report per project | P2 |
| 160 | Budget alerts at thresholds | P2 |
| 161 | Multi-currency support | P3 |
| 162 | Forecast at completion (EAC) calculation | P3 |
| 163 | Earned value metrics (PV, EV, AC, CPI, SPI) | P3 |
| 164 | Budget approval workflow | P3 |
| 165 | Cost center and accounting dimension mapping | P3 |

## 8. Planning and scheduling

| # | Feature | Tier |
|---|---|---|
| 166 | Auto-scheduling by dependencies | P2 |
| 167 | Working-day aware date calculation | MVP |
| 168 | Critical path computation | P3 |
| 169 | Slack/float calculation | P3 |
| 170 | Lag and lead on dependencies | P3 |
| 171 | Schedule conflict detection | P2 |
| 172 | Rescheduling cascade with preview | P3 |
| 173 | Deadline risk prediction (heuristic) | P3 |
| 174 | Baseline vs actual schedule comparison | P3 |
| 175 | Milestone dependency tracking | P2 |
| 176 | What-if scenario cloning | P3 |

## 9. Collaboration and communication

| # | Feature | Tier |
|---|---|---|
| 177 | Comments with @mentions on any PM doctype | MVP |
| 178 | Frappe Assignment and ToDo integration | MVP |
| 179 | Project discussion/chat thread | P2 |
| 180 | Activity feed per project | MVP |
| 181 | Document sharing with fine-grained permissions | MVP |
| 182 | Reactions/likes on comments | P3 |
| 183 | Rich text with code blocks and images in comments | MVP |
| 184 | Threaded replies | P3 |
| 185 | Announcements board per project | P3 |
| 186 | Meeting notes DocType with action items to tasks | P2 |
| 187 | Decision log | P3 |
| 188 | Team directory and profiles | P3 |
| 189 | Presence/who is viewing indicator (realtime) | P3 |
| 190 | Realtime updates via Socket.IO on boards | MVP |
| 191 | Email threads linked to tasks (Communication) | P2 |
| 192 | Daily standup report auto-generated | P3 |

## 10. Documents and knowledge

| # | Feature | Tier |
|---|---|---|
| 193 | Project documents DocType with versioning | P2 |
| 194 | Folder structure (Frappe File tree) | P2 |
| 195 | Wiki/knowledge base per project (Frappe Wiki integration) | P3 |
| 196 | Document approval workflow | P2 |
| 197 | Document templates | P3 |
| 198 | File preview for PDFs and images | MVP |
| 199 | Full-text search across tasks and docs | P2 |
| 200 | Document expiry/review reminders | P3 |
| 201 | Requirements DocType with traceability to tasks | P3 |
| 202 | Test case DocType linked to stories | P3 |
| 203 | Decision/ADR records | P3 |
| 204 | Link-to-file public share links | P3 |

## 11. Roles, permissions, and security

| # | Feature | Tier |
|---|---|---|
| 205 | Predefined roles: PM Admin, Project Manager, Team Member, Viewer, Client | MVP |
| 206 | Project-level permissions (user permissions per project) | MVP |
| 207 | Permission query conditions (members see only their projects) | MVP |
| 208 | Field-level permissions via permlevel | MVP |
| 209 | Role-based dashboards and workspaces | MVP |
| 210 | Private/confidential projects | P2 |
| 211 | Client/guest read-only access | P2 |
| 212 | Audit trail (version tracking on all doctypes) | MVP |
| 213 | Activity log of logins and key actions | P2 |
| 214 | Two-factor authentication (native Frappe) | MVP |
| 215 | SSO via OAuth/SAML/LDAP (native Frappe) | P2 |
| 216 | Rate limiting on API | P2 |
| 217 | Input sanitization and XSS protection | MVP |
| 218 | Encrypted password-type fields for credentials | P2 |
| 219 | Data retention and anonymization policy | P3 |
| 220 | GDPR export/delete personal data | P3 |
| 221 | IP allowlist option | P3 |
| 222 | Session timeout configuration | P2 |
| 223 | Share-with-expiry permissions | P3 |
| 224 | Permission matrix documentation | MVP |

## 12. Workflow and automation

| # | Feature | Tier |
|---|---|---|
| 225 | Frappe Workflow for task status transitions | MVP |
| 226 | Configurable approval workflows (timesheets, CRs, budgets) | MVP |
| 227 | Automation rules engine (trigger, condition, action) | P2 |
| 228 | Auto-assign rules (round-robin, by skill) | P2 |
| 229 | Frappe Assignment Rule presets | MVP |
| 230 | Auto-status change on dependency completion | P2 |
| 231 | Scheduled jobs (overdue checks, digest emails) | MVP |
| 232 | Server scripts / client scripts customization hooks | MVP |
| 233 | Escalation rules for overdue tasks | P2 |
| 234 | SLA policies with timers (support projects) | P3 |
| 235 | Webhook triggers on events (native Webhook DocType) | MVP |
| 236 | Recurring project/sprint creation | P3 |
| 237 | Auto-create tasks from template on project start | P2 |
| 238 | Conditional required fields per status | P2 |
| 239 | Event hooks (doc_events) for extensions | MVP |
| 240 | Zapier/n8n compatible webhooks | P3 |

## 13. Notifications

| # | Feature | Tier |
|---|---|---|
| 241 | In-app notifications (Frappe notification bell) | MVP |
| 242 | Email notifications for assignment, mention, status change | MVP |
| 243 | Notification Settings per user | MVP |
| 244 | Daily/weekly digest emails | P2 |
| 245 | Overdue and due-soon alerts | MVP |
| 246 | Push notifications (web push) | P3 |
| 247 | Slack/Teams/Telegram notification integration | P3 |
| 248 | SMS/WhatsApp notifications (Frappe SMS settings) | P3 |
| 249 | Custom Notification templates (Jinja) | MVP |
| 250 | Quiet hours and mute per project | P3 |
| 251 | Mention-only mode | P2 |
| 252 | Notification when watched task changes | MVP |

## 14. Reports and analytics

| # | Feature | Tier |
|---|---|---|
| 253 | Project summary script report | MVP |
| 254 | Task status distribution report | MVP |
| 255 | Overdue tasks report | MVP |
| 256 | Workload by user report | MVP |
| 257 | Milestone status report | P2 |
| 258 | Project progress report (planned vs actual) | P2 |
| 259 | Burndown/velocity dashboards | MVP |
| 260 | Timesheet utilization report | P2 |
| 261 | Budget variance report | P2 |
| 262 | Risk and issue summary report | P3 |
| 263 | Portfolio dashboard across projects | P2 |
| 264 | Custom dashboard charts (Frappe Dashboard Chart) | MVP |
| 265 | Query reports with user-editable filters | MVP |
| 266 | Scheduled report emails (Auto Email Report) | P2 |
| 267 | Report export to PDF/Excel | MVP |
| 268 | Period-over-period comparison | P3 |
| 269 | Executive summary dashboard | P2 |
| 270 | Throughput and completion trend | P2 |
| 271 | Estimation accuracy report | P3 |
| 272 | Team performance (non-punitive) insights | P3 |
| 273 | Custom report builder (native) | MVP |

## 15. Client portal

| # | Feature | Tier |
|---|---|---|
| 274 | Customer portal listing their projects | P2 |
| 275 | Portal task/milestone view with read-only status | P2 |
| 276 | Client feedback and approval on deliverables | P3 |
| 277 | Client ticket/request submission web form | P2 |
| 278 | Portal file sharing with clients | P3 |
| 279 | Portal comments visible to client | P3 |
| 280 | Branded portal with logo and colors | P3 |
| 281 | Public project status page (optional share link) | P3 |
| 282 | Portal notifications | P3 |
| 283 | Client timesheet/invoice visibility | P3 |

## 16. Integrations

| # | Feature | Tier |
|---|---|---|
| 284 | GitHub integration: link commits/PRs to tasks | P2 |
| 285 | GitLab/Bitbucket integration | P3 |
| 286 | Google Calendar sync (Frappe native) | P2 |
| 287 | Google Drive file linking | P3 |
| 288 | Slack integration | P3 |
| 289 | ERPNext integration (customers, invoices, expenses) | P2 |
| 290 | HRMS integration (employees, leave) | P3 |
| 291 | Frappe Helpdesk integration (ticket to task) | P3 |
| 292 | Frappe CRM integration (deal to project) | P3 |
| 293 | iCal export feed | P2 |
| 294 | Email in/out via Frappe Email Account | MVP |
| 295 | CSV/Excel import and migration from Jira, Trello, Asana | P3 |
| 296 | Webhook outbound events | MVP |
| 297 | REST API tokens (native API key/secret) | MVP |
| 298 | OpenAPI/Swagger documentation | P3 |
| 299 | Outlook calendar sync | P3 |
| 300 | Zoom/Meet link on meeting docs | P3 |

## 17. REST API and developer features

| # | Feature | Tier |
|---|---|---|
| 301 | Whitelisted API methods for projects/tasks/sprints | MVP |
| 302 | Standard Frappe REST resources for all DocTypes | MVP |
| 303 | Bulk-operation API endpoints | P2 |
| 304 | API versioning namespace (pm.api.v1) | P2 |
| 305 | Realtime event publishing API | P2 |
| 306 | API usage logging | P3 |
| 307 | SDK/examples (Python, JS, curl) | P3 |
| 308 | GraphQL-style filtered query endpoint | P3 |
| 309 | Custom app hooks/extension points documented | P2 |
| 310 | Fixtures for roles, workflows, and templates | MVP |

## 18. Admin and settings

| # | Feature | Tier |
|---|---|---|
| 311 | PM Settings single DocType (defaults, working days) | MVP |
| 312 | Custom status/priority/type masters | MVP |
| 313 | Numbering series per project | MVP |
| 314 | Default project templates setup wizard | MVP |
| 315 | Role/permission setup on install | MVP |
| 316 | Branding settings (logo, accent color) | P3 |
| 317 | Feature toggles (enable sprints, budgets, portal) | P2 |
| 318 | Data import/export tools | MVP |
| 319 | Demo data generator | P2 |
| 320 | Backup/restore guidance (bench) | MVP |
| 321 | Health check page (scheduler, queue status) | P3 |
| 322 | Multi-company support | P2 |
| 323 | Multi-site/multi-tenant ready design | P2 |
| 324 | Currency and timezone settings | MVP |
| 325 | Language/translation management | MVP |
| 326 | Telemetry opt-out controls | P3 |

## 19. Internationalization and accessibility

| # | Feature | Tier |
|---|---|---|
| 327 | All strings wrapped with translation function (__) | MVP |
| 328 | Translation CSVs for Arabic, Spanish, French, German | P2 |
| 329 | RTL layout support | P2 |
| 330 | Date, number, and currency locale formatting | MVP |
| 331 | WCAG-aware color contrast and keyboard navigation | P2 |
| 332 | Timezone-aware due dates | MVP |
| 333 | Screen-reader labels on custom UI | P3 |
| 334 | Localized email templates | P3 |

## 20. UX and productivity

| # | Feature | Tier |
|---|---|---|
| 335 | Global search and awesomebar integration | MVP |
| 336 | Keyboard shortcuts (create task, search, navigate) | P2 |
| 337 | Command palette | P3 |
| 338 | Quick filters and saved filters | MVP |
| 339 | Onboarding tour for new users | P2 |
| 340 | Empty-state guidance | P2 |
| 341 | Inline editing in list views | P2 |
| 342 | Drag and drop attachments | MVP |
| 343 | Personal Today dashboard (due, overdue, upcoming) | MVP |
| 344 | Mobile-responsive desk and portal | MVP |
| 345 | PWA installable | P3 |
| 346 | Undo for recent bulk edits | P3 |
| 347 | Autosave drafts | MVP |
| 348 | Task templates quick insert | P2 |
| 349 | Pomodoro/focus mode | P3 |
| 350 | Customizable card fields on boards | P2 |

## 21. AI-assisted features (optional)

| # | Feature | Tier |
|---|---|---|
| 351 | AI task description and acceptance-criteria drafting | P3 |
| 352 | Summarize long comment threads | P3 |
| 353 | Auto-generate project status updates | P3 |
| 354 | Duplicate task detection | P3 |
| 355 | Smart estimate suggestions from history | P3 |
| 356 | Natural-language task creation | P3 |

## 22. Performance and reliability

| # | Feature | Tier |
|---|---|---|
| 357 | Indexed fields for common filters | MVP |
| 358 | Background jobs for heavy rollups (queue) | MVP |
| 359 | Redis caching of dashboard counts | P2 |
| 360 | Pagination and lazy loading in boards | MVP |
| 361 | Query optimization with report-level limits | MVP |
| 362 | Idempotent patches/migrations | MVP |
| 363 | Error logging with Frappe Error Log | MVP |
| 364 | Graceful handling of concurrent edits (timestamp check) | MVP |
| 365 | Load-tested at 100k tasks target | P3 |
| 366 | Rollup recomputation scheduled safeguard | P2 |

## 23. Testing, quality, and deployment

| # | Feature | Tier |
|---|---|---|
| 367 | Unit tests for core DocTypes (FrappeTestCase) | MVP |
| 368 | Integration tests for workflows and permissions | MVP |
| 369 | API tests | MVP |
| 370 | UI tests (Cypress/Playwright) | P2 |
| 371 | CI via GitHub Actions (tests, lint, build) | MVP |
| 372 | Pre-commit: ruff, eslint, prettier | MVP |
| 373 | Semgrep/security linting | P2 |
| 374 | Dependabot configuration | P3 |
| 375 | Dockerfile/compose for dev and prod | P2 |
| 376 | bench install-app instructions | MVP |
| 377 | Frappe Cloud marketplace readiness | P3 |
| 378 | Semantic versioning and CHANGELOG | MVP |
| 379 | Contributing and developer docs | MVP |
| 380 | User manual and admin guide | MVP |
| 381 | Migration patches between versions | MVP |
| 382 | License and README | MVP |
