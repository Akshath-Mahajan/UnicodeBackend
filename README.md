# Progression Timeline
This project is my work during DJ Unicode LP for backend.

## Objective
The goal of this app is to build a backend to keep track of a person's progress (during lockdown for example)

## Features
A person can create lists, and each list can have multiple tasks within it. When you mark a task as complete, that date gets stored and you can thus review what goals you accomplished on a certain day.

## General backend
You can login and signup as well as perform CRUD operations on lists and tasks using the normal urls provided. Your lists and tasks will only be maintained by you
## Rest Framework
Endpoints for login, signup and CRUD operations have been added using DRF. Token authentication as well as permission checks have also been included.
IsAuthenticated is the default permission class set for DRF, and we do exempt from it in the login/signup endpoint. 
