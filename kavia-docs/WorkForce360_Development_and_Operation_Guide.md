# WorkForce360 Development Plan & kavia.ai Usage Guide

---

## Introduction

Welcome to WorkForce360! This document is a complete, step-by-step reference for onboarding new team members and guiding development of the WorkForce360 system—a modern platform for managing employee timesheets, tasks, roles and permissions, and leave. It is also your comprehensive guide to leveraging the kavia.ai code generation and agent-based workflow for a streamlined and productive development journey.

This guide covers:
- The project structure and core features of WorkForce360
- A quick-start primer on using kavia.ai tooling and agent workflows
- Detailed, phase-by-phase development instructions with best practices
- Guidance on agent roles, assignment strategies, and troubleshooting common issues

---

## Project Overview

WorkForce360 is designed as a full-stack application comprised of a FastAPI backend and a Vite-powered JavaScript frontend. Its major features include:

- **Timesheet Logging**: Detailed, calendar-based timesheet entries
- **Task Management**: Flexible CRUD operations and task assignments
- **Role-Based Access Control (RBAC)**: Granular user permissions
- **Leave Management**: Submission, approval, and tracking of employee leave
- **Dashboards**: Managerial overviews of team activities

The backend codebase resides in the `backend/` directory, while the frontend is contained within `/workforce360/`.

---

## kavia.ai Quick Start for New Users

kavia.ai is an AI-powered collaborative platform utilizing specialized “agents” (e.g., PlanningAgent, CodeWritingAgent, TestCodeWritingAgent) to automate and accelerate software development. Here’s how best to get started:

### Workflow Basics

1. **Tasks and Subtasks**: All work is described as tasks (e.g., “Implement Leave API”) and is broken down into granular, actionable subtasks.
2. **Agents**: Each subtask is assigned to an agent best suited to the activity—coding, testing, planning, documentation, etc.
3. **Command Format**: Interactions (prompts) with kavia.ai should clearly express the goal and context. Avoid ambiguous wording—be direct and specific.
4. **Observability**: Agent tool actions (like editing or creating files) are logged and can be reviewed for audit/troubleshooting.

### Standard Procedures

- **Starting the Backend**:  
  Run from `/backend`:
  ```
  source venv/bin/activate && uvicorn src.api.main:app --host 0.0.0.0 --port <port> --reload
  ```
- **Running Backend Tests**:  
  Run from `/backend`:
  ```
  pytest
  ```
- **Starting the Frontend**:
  Run from `/workforce360`:
  ```
  npm install
  npm run dev
  ```

### Best Practices for Agent Assignment

- Use `PlanningAgent` for roadmap creation and analysis of codebase structure.
- Assign implementation subtasks to `CodeWritingAgent`.
- Assign `TestCodeWritingAgent` and `TestExecutionAgent` to automate test writing and validation.
- Use `DocumentationAgent` early and throughout to keep all documentation up-to-date.
- For issues/bugs, assign `BugFixingAndVerificationAgent` after reproducing the problem.
- Use `HelpAgent` if uncertain about agent capabilities or proper process.

---

## Phase 1: Project Setup & Familiarization

1. **Clone the repository** and explore the folder structure:
   - `/backend/` for the FastAPI backend
   - `/workforce360/` for the Vite JavaScript frontend
   - `README.md` for high-level info
2. **Read the README.md** for quick orientation.
3. **Set up Python environment** for the backend. Use a virtual environment.
4. **Install backend dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```
5. **Start the backend and verify the health-check endpoint** at `/`.
6. **Set up Node.js environment** for the frontend.
7. **Run frontend install/build commands** in `/workforce360`.

---

## Phase 2: Backend Foundations (FastAPI & Database)

1. **Plan database schema** for users, roles, permissions, timesheets, tasks, and leave requests.
2. **Implement database models** using SQLAlchemy or Pydantic as per FastAPI conventions.
3. **Add migration scripts** (Alembic or preferred tool).
4. **Establish database connection logic** in backend code.
5. **Test with basic data creation and retrieval** endpoints.
6. **Document database schema and endpoint paths** using OpenAPI or markdown.

#### kavia.ai Sample Prompts
- “Write a Timesheet SQLAlchemy model and migration script.”
- “Generate FastAPI endpoints for CRUD operations on Task.”

---

## Phase 3: Backend Feature APIs

For each core API (Timesheet, Task, User/Role, Leave, Dashboard):

1. **Design RESTful endpoint structure** (`/timesheets/`, `/tasks/`, etc.).
2. **Implement endpoints**: GET (list/detail), POST, PUT/PATCH, DELETE.
3. **Integrate input validation** using Pydantic schemas.
4. **Add business logic (who can do what)**.
5. **Write automated tests** for each API route.
6. **Document all endpoints** (OpenAPI/Swagger and markdown).

#### Agent Guidance

- Assign one agent per API or resource area for maximum focus.
- Use `TestCodeWritingAgent` after every new endpoint.
- Update documentation in parallel to implementation for accuracy.

---

## Phase 4: Backend Security, RBAC & Testing

1. **Implement authentication** (JWT/Bearer token or OAuth2).
2. **Develop reusable RBAC decorators/middleware** for endpoint protection.
3. **Fully test permission boundaries** and user flows.
4. **Integrate CORS and security best practices** in FastAPI settings.
5. **Run pytest to validate all test cases and coverage**.
6. **Patch vulnerabilities and document all security practices**.

---

## Phase 5: Frontend Foundations

1. **Bootstrap the Vite app (`npm create vite@latest` or use the existing `/workforce360/`)**.
2. **Setup project configuration**, linting (eslint), and code style (Prettier, if desired).
3. **Establish folder structure** for views/pages, components, API utilities, and state management (if used).
4. **Create basic navigation shell and main layout** (tabbed navigation, side-panel, status tag displays).
5. **Verify frontend launches and displays basic scaffolding**.

---

## Phase 6: Frontend Feature Development

For each feature:

1. **Design UI/UX wireframes or use supplied designs**.
2. **Build reusable components** for forms (timesheet, task creation, leave requests, etc.).
3. **Wire up frontend API calls** to backend endpoints using fetch/axios.
4. **Manage user authentication and role-enforced UI logic**.
5. **Add client-side form validation and error handling**.
6. **Write unit and integration tests for key user flows**.
7. **Continuously update help texts, tooltips, and UI documentation**.

---

## Phase 7: Frontend/Backend Integration

1. **Test all data flows between frontend and backend**.
2. **Simulate real-world user scenarios (manager, employee, etc.)**.
3. **Fix CORS or communication issues as they arise**.
4. **Polish user feedback and UI responsiveness based on data endpoints**.
5. **Close gaps in API contracts with backend as discovered**.
6. **Document usage patterns for API and UI**.

---

## Phase 8: Documentation & Product Polish

1. **Audit all project documentation (README, API docs, onboarding guides, etc.)** and update for accuracy and completeness.
2. **Write or update onboarding instructions for new developers**.
3. **Add architectural descriptions and diagrams** to clarify system interfaces and flow.
4. **Ensure test coverage is above required minimum and code meets linting/quality gates**.
5. **Prepare deployment instructions (both local and cloud, if required)**.
6. **Conduct last full manual walkthrough (“bug bash”) with the team**.

---

## Helpful Hints & Troubleshooting

- **Agent Guidance**: If a task isn’t moving forward, check that the correct agent is assigned and it has adequate context.
- **Common Command Issues**: Many problems are typos or missing dependencies—always read logs and agent feedback.
- **Debugging**: Use the logging output from both FastAPI and Vite dev servers for error diagnosis. Assign `BugFixingAndVerificationAgent` if repeated issues arise.
- **Documentation**: Use the `DocumentationAgent` regularly to sync changes.
- **Security**: Before launch, double-check CORS, JWT secrets, and protected route access.

---

## Appendix: Agent Assignment Cheat Sheet

| Task Type            | Recommended Agent                  |
|----------------------|-----------------------------------|
| Roadmap Planning     | PlanningAgent                     |
| Code Implementation  | CodeWritingAgent                  |
| Unit Testing         | TestCodeWritingAgent              |
| Integration Testing  | TestExecutionAgent                |
| Bug Diagnosis        | BugFixingAndVerificationAgent     |
| UI Asset Extraction  | DesignExtractionAgent             |
| Coding Questions     | QuestionAnsweringAgent            |
| Documentation        | DocumentationAgent                |
| General Tasks        | GeneralistAgent                   |
| Help/Process Info    | HelpAgent                         |

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vite Documentation](https://vitejs.dev/)
- [kavia.ai User Help](https://docs.kavia.ai/)
- For project-specific files, see `/backend/` and `/workforce360/` directories.

---

This concludes the onboarding and execution guide for WorkForce360. All team members should refer to this document as the single source of truth for process, coding standards, and kavia.ai usage throughout the project lifecycle.
