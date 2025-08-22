# 🛡️ API Blocking & Safety Filter Guide

This guide helps you understand and resolve issues when the AI model blocks responses due to safety filters.

## 🚨 Understanding the Error

### What is `finish_reason: 1`?
When you see this error:
```
Invalid operation: The `response.text` quick accessor requires the response to contain a valid `Part`, but none were returned. The candidate's finish_reason is 1.
```

This means the AI model's safety filters blocked the response because it detected potentially inappropriate content.

### Finish Reason Codes
- **1 (BLOCKED)**: Response blocked by safety filters
- **2 (STOP)**: Response completed normally
- **3 (MAX_TOKENS)**: Response truncated due to token limit

## 🔧 Solutions

### 1. Rephrase Your Question

**Instead of:**
```
"Solve this problem about guns and bullets"
```

**Try:**
```
"Solve this physics problem about projectile motion"
```

### 2. Use Academic Language

**Instead of:**
```
"Help me hack into a system"
```

**Try:**
```
"Explain cybersecurity concepts and encryption methods"
```

### 3. Focus on Mathematical Content

**Instead of:**
```
"Calculate the damage from an explosion"
```

**Try:**
```
"Calculate the area and volume of a spherical object"
```

## 📝 Best Practices

### ✅ Do's
- Use academic, educational language
- Focus on mathematical concepts
- Use standard mathematical notation
- Break complex problems into simpler parts
- Use neutral, professional terminology

### ❌ Don'ts
- Reference weapons, violence, or harmful content
- Use potentially controversial topics
- Include inappropriate or offensive language
- Reference illegal activities
- Use overly complex or ambiguous language

## 🎯 Common Triggers

### Topics That May Be Blocked
- Weapons and ammunition
- Violence and harm
- Illegal activities
- Controversial political topics
- Inappropriate content
- Potentially harmful instructions

### Safe Mathematical Topics
- Algebra and equations
- Geometry and shapes
- Calculus and derivatives
- Statistics and probability
- Trigonometry
- Linear algebra
- Number theory
- Mathematical proofs

## 🔄 How to Retry

### Step 1: Identify the Trigger
Look at your original question and identify what might have triggered the safety filter.

### Step 2: Rephrase
Use more academic, neutral language that focuses on the mathematical content.

### Step 3: Simplify
Break down complex problems into simpler, more focused questions.

### Step 4: Test
Try your rephrased question and see if it works.

## 💡 Example Transformations

### Example 1: Physics Problem
**Blocked:**
```
"Calculate the trajectory of a bullet fired from a gun"
```

**Safe:**
```
"Calculate the parabolic trajectory of a projectile with initial velocity v₀ and angle θ"
```

### Example 2: Chemistry Problem
**Blocked:**
```
"Calculate the explosion force of a bomb"
```

**Safe:**
```
"Calculate the energy released in a chemical reaction using the given equation"
```

### Example 3: Biology Problem
**Blocked:**
```
"Calculate the lethal dose of a poison"
```

**Safe:**
```
"Calculate the concentration of a substance in a solution using dilution factors"
```

## 🛠️ Technical Solutions

### 1. Use Safer Prompts
The application now uses safer, more academic prompts by default.

### 2. Check Response Validation
The system now validates responses and provides clear error messages.

### 3. Get Suggestions
When blocked, the system provides suggestions for rephrasing your question.

## 📊 Monitoring and Logging

### Log Messages to Watch For
```
Gemini response was blocked by safety filters
AI response was blocked by safety filters. Please try rephrasing your question.
```

### Debug Information
Enable DEBUG logging to see detailed information:
```env
LOG_LEVEL=DEBUG
```

## 🆘 Getting Help

### If You're Still Having Issues

1. **Check the logs** for detailed error information
2. **Try a different approach** to the same problem
3. **Break down the problem** into smaller parts
4. **Use more specific mathematical terminology**
5. **Avoid any potentially controversial content**

### Contact Support
If you continue to have issues:
1. Share the exact error message
2. Include your original question (if appropriate)
3. Describe what you're trying to accomplish
4. Mention any rephrasing attempts you've made

## 🎓 Educational Focus

Remember, this is an educational tool designed for:
- Learning mathematics
- Understanding concepts
- Solving academic problems
- Improving mathematical skills

Keep your questions focused on these educational goals, and you should avoid most blocking issues.

## 🔍 Troubleshooting Checklist

- [ ] Question uses academic language
- [ ] Focus is on mathematical content
- [ ] No references to weapons or violence
- [ ] No potentially controversial topics
- [ ] Clear, specific mathematical problem
- [ ] Standard mathematical notation
- [ ] Educational context maintained

Happy learning! 📚✨ 