# OBJECTIVE:
Modify the provided JavaScript function `doSomething` to accept a `name` parameter and print its value to the console.

## CONTEXT:
The provided file `dummy_code.js` contains a JavaScript function named `doSomething` which currently prints a static string. The goal is to update this function to be dynamic, accepting and printing a user-provided name.

## SOURCE FILES:
```
dummy_code.js
```
```javascript
function doSomething() {
 console.log('hello');
}
```

## INSTRUCTIONS & STEPS:
1.  **Locate Function:** Identify the `doSomething` function within the `<file_content>` of `dummy_code.js`.
2.  **Modify Signature:** Update the function signature of `doSomething` to accept a single parameter named `name`.
3.  **Update Logic:** Change the `console.log` statement inside the function to print the value of the `name` parameter instead of the static string 'hello'.

## CONSTRAINTS & GUARDRAILS:
*   Only modify the `doSomething` function. No other code should be added, removed, or altered.
*   The function must continue to use `console.log()` for printing.
*   The output must be syntactically correct JavaScript.
*   Do not include any conversational filler or explanations in the output.

## EXPECTED OUTPUT FORMAT:
The complete, modified content of the `dummy_code.js` file, enclosed within a markdown code block for JavaScript.

```javascript
// [Your modified JavaScript code here]
```