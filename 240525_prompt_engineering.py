
def what_is_your_role(task):
  if task == "writing prompts":
    return "Prompt Engineer"
  elif task == "Margaritas Maker":
    return "Chemical Engineer"
  else:
    return "We are still exploring... YOU engineer"

role = what_is_your_role("writing prompts")

print(f"Your role: {role}")


