<img width="1034" height="823" alt="Screenshot 2026-06-12 at 8 18 57 AM" src="https://github.com/user-attachments/assets/6d5e165c-5a8c-4245-947c-01866e6d33c2" />
<img width="1411" height="576" alt="Screenshot 2026-06-12 at 8 20 39 AM" src="https://github.com/user-attachments/assets/c3122116-9cf8-4f17-b185-fa55e8f08fea" />
<img width="1410" height="579" alt="Screenshot 2026-06-12 at 8 21 15 AM" src="https://github.com/user-attachments/assets/ffa37aa1-c82d-464d-919b-78b146c222b5" />


# Role-Based Access Control & REST API Integration - Task 4

## Overview
This project upgrades our existing Flask-based CRUD application into an enterprise-ready backend system. It introduces Role-Based Access Control (RBAC) to separate standard users from administrators, and implements RESTful API endpoints to allow external systems to interact with the database using JSON.

## Role Logic & Authorization (RBAC)
To manage user permissions, a `role` column was added to the SQLite `users` table, defaulting to 'user', with specific accounts elevated to 'admin'. 
* **Session Storage:** Upon successful login, the application saves both the user's username and their specific `role` into the secure Flask session.
* **The Custom Decorator:** A custom Python decorator (`@admin_required`) was built to wrap specific administrative routes. 
* **Admin Capabilities:** Users with the 'admin' role are granted access to a specialized `/admin` dashboard to view all registered accounts. Additionally, critical actions, such as deleting a student record, are now strictly protected by the `@admin_required` decorator, preventing standard users from executing destructive commands.

## REST API Endpoints
Alongside the visual web interface, the application now exposes a set of REST API endpoints under `/api/students` to handle raw data operations. These routes bypass HTML rendering and return standard JSON responses, making the backend compatible with mobile apps or frontend frameworks.
* **GET `/api/students`:** Fetches all student records and returns them as a JSON array.
* **POST `/api/students`:** Accepts a JSON payload containing `name`, `email`, and `course`, and inserts a new student into the database.
* **PUT `/api/students/<id>`:** Accepts a JSON payload and updates the specific student matching the provided ID.
* **DELETE `/api/students/<id>`:** Deletes the specific student matching the provided ID from the database.

## Security Flow
The application implements layered security:
1. **Public Layer:** Unauthenticated users are strictly redirected to `/login` or `/register`.
2. **Authenticated Layer (User):** Logged-in users are granted a session badge. They can view the standard `/dashboard`, access the visual `/students` list, and add or edit students. They cannot delete records or view other users.
3. **Elevated Layer (Admin):** Admins possess an elevated session badge. They can access all standard features, plus the `/admin` control panel, and have the exclusive authority to delete database records. Any unauthorized attempt to hit an admin route immediately redirects the user back to their designated dashboard.
