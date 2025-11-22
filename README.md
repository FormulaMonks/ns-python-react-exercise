# Welcome, Future Teammate!

Hey there! Thanks for taking the time to do this exercise. We've designed it to be a fun and challenging way to get a feel for the kind of work we do here. It's a chance for you to showcase your skills as a builder, problem-solver, and mentor across the full stack.

This isn't a typical coding test with a single right answer. We're much more interested in your thought process, how you handle trade-offs, and your ability to navigate a pre-existing (and slightly imperfect) codebase using a realistic Git workflow.

**A Quick Note on Time:** We estimate this exercise could take between 2 to 4 hours. However, we've intentionally included more work than can be done in that time. **Please do not feel pressured to complete everything.** Prioritization is a key skill, and we want to see how you approach a task with real-world time constraints.

## The Scenario: A FinTech Transaction Dashboard

You've just joined a new team building a dashboard for visualizing financial transactions. The application is composed of a Python (FastAPI) backend and a React (TypeScript) frontend. Your mission is to get familiar with the codebase, review a teammate's contribution, fix some underlying issues, and then build out a new feature.

---

## Your Mission: A Three-PR Workflow

**Important First Step:** Before you begin, please **fork this repository** (Make sure you fork all the branches, you will need them).

You will work entirely on your own fork, creating pull requests within that repository. **Do not create any pull requests to the original upstream repository.**

Your work will be organized into three separate pull requests within your own repository. We recommend following these steps in order.

### A Quick Glossary of Branches

*   **`main`**: The initial state of the codebase. You will branch from here.
*   **`fix-bug-666`**: A simulated PR from a junior developer. This branch contains their work for you to review.
*   **`fix/haunted-codebase`**: The branch you will create from `main` to fix the existing technical debt.
*   **`feature/transaction-tags-grid`**: The branch you will create from `fix/haunted-codebase` for the new feature (database migration and data grid).


### Step 0: Getting Up and Running

1.  **Clone Your Fork:** Clone your newly forked repository to your local machine.
2.  **Set Up Environment:** We've included a `docker-compose.yml` file for setup. You'll need to create a `.env` file from the `.env.example` template.
3.  **Launch the App:** Run `docker-compose up --build`. This will spin up the backend, frontend, and database. The database will be automatically seeded with initial data the first time it starts.
4.  **Explore:** The frontend is at `http://localhost:3000` and the API docs are at `http://localhost:8000/docs`. Get a feel for the app and the code on the `main` branch.

### Running Tests

We have set up a comprehensive testing suite for this project. A helper script is provided to run all tests and install any necessary dependencies automatically.

From the root of the `ns-python-react-exercise` directory, run the test script:
```bash
./run-tests.sh
```
This will execute the backend tests (unit, integration, E2E) and the frontend Playwright E2E tests.

### PR #1: The Code Review

Your first task is to act as a mentor and review a "PR" from a junior developer.

1.  **Understand the Context:** The junior dev's work is on the `fix-bug-666` branch. On that branch, read the `BUG-666.md` file to understand the original problem.
2.  **Open the PR:** In your own repository, open a pull request from `fix-bug-666` to your `main` branch. Use the PR description template below.
3.  **Perform the Review:** Go to the "Files Changed" tab of the PR you just created. Leave comments directly on the code, providing a mix of high-level architectural feedback and specific line-by-line notes.
4.  **Abandon the PR:** Once your review is complete, **close the pull request without merging.**

#### PR #1 Description Template
```md
### What I Did
This PR fixes the transaction display bug by filtering transactions on the frontend to only show relevant entries. I've also implemented server-side pagination for better performance.

### How to Test
1. Checkout this branch.
2. Run `docker-compose up --build`.
3. Navigate to the frontend at `http://localhost:3000`.
4. Observe that only relevant transactions are displayed.
5. Verify that pagination controls are now active and functional.

### Architectural Decision Record (ADR)
To address the display bug, I decided to handle filtering directly in the frontend component. This approach simplifies the backend and leverages the client's processing power for a snappier user experience. For pagination, I added a new `GET` parameter `page` and `page_size` to the existing `/api/v1/transactions/` endpoint, and updated the frontend to send these parameters.

### AI Usage Summary
I used AI tools for minor code refactoring and to generate some boilerplate for the frontend pagination component.
```

### PR #2: Fixing Technical Debt

Now, it's time to fix the *other* bugs lurking in the `main` branch.

1.  **Create a Branch:** From your `main` branch, create a new branch. We suggest `fix/haunted-codebase`.
2.  **Hunt the Bugs:** Investigate the following reports:
    *   **Backend Report:** "Users are reporting that the main transaction list is loading very slowly, especially for users with many transactions. Our initial investigation suggests the API endpoint might be making an excessive number of database calls."
    *   **Frontend Report:** "The product owner noticed that when they hover over their user profile icon in the header, the main data grid seems to flicker and re-render, even though the data hasn't changed. This is causing a sluggish feel on the dashboard. The React Profiler might be useful for confirming this."
3.  **Open the PR:**
    *   Open a new pull request in your repository from `fix/haunted-codebase` to `main`.
    *   Use the PR description template for PRs #2 and #3 below.
    *   **Leave this pull request open** for us to review.

### PR #3: New Feature Development (Stacked PR)

With the codebase stabilized, you can now build the new feature. This PR will be "stacked" on top of PR #2, meaning it builds directly on the changes made in `fix/haunted-codebase`.

1.  **Create a Branch:** From your `fix/haunted-codebase` branch, create a new branch. We suggest `feature/transaction-tags-grid`.
    *   *Note: Because this is a "stacked" PR, you will see the commits from your `fix/haunted-codebase` branch also included in this pull request. This is expected.*

2.  **The "Twist": Database Schema Evolution**
    The core of this new feature is to enable a transaction to have **multiple associated tags** (e.g., "work", "travel", "reimbursable") instead of just a single category.
    *   **Current State:** A `Transaction` currently has a many-to-one relationship with a `Category`.
    *   **Required Change:** Evolve the schema to allow a **many-to-many relationship** between `Transaction` and `Tag`. Design and implement the necessary database schema changes (e.g., new `Tag` model, an association table) and update the `backend/seed.py` script to populate some sample tags and associations. Since there's no dedicated migration tool, manual schema updates followed by `docker-compose down -v && docker-compose up --build` will be sufficient to apply your changes.

3.  **Build the Feature:**
    *   **Backend (Python/FastAPI):**
        *   Create a **new API endpoint** (e.g., `GET /api/v1/transactions/grid`) specifically designed to serve the advanced needs of the new data grid. This new endpoint should be distinct from existing transaction endpoints to avoid breaking changes and allow for specialized optimization for the grid's requirements (such as multi-table joins and aggregated tag data).
        *   This endpoint should support **server-side pagination** (e.g., `page`, `size` query parameters) and **server-side sorting** (e.g., `sort_by`, `sort_order` query parameters).
        *   The endpoint's data fetching logic **must use a raw SQL query with a multi-table `JOIN`** to retrieve transactions along with their associated categories and *all* their new tags.
        *   The response should be structured to facilitate rendering in a data grid, ideally including the total count of transactions for pagination purposes.
    *   **Frontend (React/TypeScript):**
        *   Build a **new React component** (e.g., `TransactionGrid.tsx`) that displays transactions in a **data grid**.
        *   This grid should display columns for `Date`, `Description`, `Amount`, `Category`, and a new column to show the **associated tags** for each transaction (e.g., as colored pills or badges).
        *   Implement **server-side sorting**: Clicking on column headers (e.g., `Date`, `Amount`) should trigger an API call to the new backend endpoint with the appropriate `sort_by` and `sort_order` parameters.
        *   Implement **server-side pagination**: Add controls (e.g., "Previous", "Next" buttons, page numbers) that interact with the new backend endpoint using `page` and `size` parameters.
        *   You are not required to add new third-party data grid libraries; building it with standard HTML table elements is perfectly acceptable and often preferred to demonstrate core React and UI skills.
4.  **Open the PR:**
    *   Open a new pull request from `feature/transaction-tags-grid` to your `main` branch.
    *   Use the PR description template for PRs #2 and #3 below. In your description, please explicitly mention that this PR builds on `fix/haunted-codebase` and link to PR #2.
    *   **Leave this pull request open** for us to review.

---

## The Deliverable

The final deliverable is **a link to your forked repository.** When you submit it, we expect to see the following:

*   **PR #1 (Code Review):** A **closed** pull request from `fix-bug-666` to `main`, containing your review comments.
*   **PR #2 (Bug Fixes):** An **open** pull request from `fix/haunted-codebase` to `main`, containing the fixes.
*   **PR #3 (New Feature):** An **open** pull request from `feature/transaction-tags-grid` to `main`, containing the database migration and the new data grid feature. This PR will implicitly include the commits from PR #2 as its base.

### PR Description Template for PRs #2 and #3

For PRs #2 and #3, please use this template:

```md
### What I Did
(A brief summary of the changes in this PR.)

### Depends On
(If this PR builds on another, like PR #3 builds on PR #2, link it here.)

### How to Test
(Clear instructions on how to test the changes in this PR.)

### Architectural Decision Record (ADR)
(A short explanation of significant decisions. For PR #3, this should cover the DB migration and state management.)

### AI Usage Summary
(A high-level summary of how you used AI tools.)
```

---

Good luck, and have fun! We're excited to see your work.