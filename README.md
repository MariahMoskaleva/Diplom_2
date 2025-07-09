diff --git a/README.md b/README.md
index 1828f67d6675f5d50091ad40a038665e06f5120d..997b289d06c5c0d50df8a97c440797ad865ca1b4 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,34 @@
-Автоматические тесты проекта Stellar Burgers. Используется pytest, requests, allure-report
+# Stellar Burgers API tests
+
+Automated tests for the Stellar Burgers project. Pytest and Allure are used for test execution and reporting.
+
+## Setup
+
+Install the dependencies listed in `requirements.txt`:
+
+```bash
+pip install -r requirements.txt
+```
+
+The tests require two environment variables that can be placed in a `.env` file or exported in your shell:
+
+- `BASE_URL` – the base address of the API under test.
+- `DEFAULT_HEADERS` – default HTTP headers sent with every request (for example `{"Content-Type": "application/json"}`).
+
+`python-dotenv` will load variables from a `.env` file automatically when the tests run.
+
+## Running tests
+
+Execute the test suite with:
+
+```bash
+pytest -vv
+```
+
+To generate an Allure report you can run:
+
+```bash
+pytest --alluredir=./allure-results
+allure serve ./allure-results
+```
+
