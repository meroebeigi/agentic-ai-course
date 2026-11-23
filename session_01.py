"""Session 1: Python Refresher and Object-Oriented Programming.

Run with Python 3.12+: python session_01.py
Course: https://github.com/ReDI-Aarhus/Agentic-AI/tree/main/classes/01-python-refresher-oop
Lecture slides 32–34 supply BankAccount, Student, and WorkoutSession.

The setup homework reviews Python environment setup and language basics.
For the official environment, run `uv sync` from the course project directory,
then run `uv run jupyter lab` to follow its tutorial. This standalone solution
uses only the Python standard library and can run directly.
"""
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import re
from typing import TypedDict


# A0–A5: Types, control flow, functions, dictionaries, and exceptions.
name = "Sam Rivera"  # str
date_of_birth = "1990-04-12"  # str
age = 36  # int
is_paid_member = True  # bool
membership_price = 12.50  # float


def classify_temperature(celsius):
    if celsius <= 0:
        return "freezing"
    if celsius <= 15:
        return "cold"
    if celsius <= 25:
        return "mild"
    return "hot"


def build_greeting(name, greeting="Hello", **details):
    message = f"{greeting}, {name}!"
    if details:
        pairs = ", ".join(f"{key}: {value}" for key, value in details.items())
        return f"{message} ({pairs})"
    return message


def pending_tasks_by_priority(tasks):
    pending = [task for task in tasks if not task["done"]]
    return [task["name"] for task in sorted(pending, key=lambda task: task["priority"])]


def count_by_priority(tasks):
    counts = {}
    for task in tasks:
        priority = task["priority"]
        counts[priority] = counts.get(priority, 0) + 1
    return counts


def count_by_priority_comprehension(tasks):
    return {p: sum(t["priority"] == p for t in tasks) for p in {t["priority"] for t in tasks}}


def flaky_divide(a, b):
    return a / b


def safe_call(func, a, b):
    try:
        return func(a, b)
    except ZeroDivisionError:
        return "error: division by zero"
    except Exception as error:
        return f"error: {type(error).__name__}"


# B1–B4: Task instances, shared counters, composition, and a local agent.
class Task:
    total_created = 0

    def __init__(self, name, priority):
        self.name = name
        self.priority = priority
        self.done = False
        Task.total_created += 1

    def mark_done(self):
        self.done = True

    def __str__(self):
        status = "x" if self.done else " "
        return f"[{status}] {self.name} (priority {self.priority})"


class TaskList:
    def __init__(self):
        self.tasks = []

    def add(self, task):
        self.tasks.append(task)

    def pending(self):
        return sorted((task for task in self.tasks if not task.done), key=lambda task: task.priority)

    def __len__(self):
        return len(self.tasks)


class SimpleAgent:
    def __init__(self, name, task_list):
        self.name = name
        self.task_list = task_list

    def act(self):
        pending = self.task_list.pending()
        if not pending:
            return f"{self.name}: nothing to do!"
        task = pending[0]
        task.mark_done()
        return f"{self.name}: working on '{task.name}'"


# Lecture exercises and homework: Bank Account, Student Profile, Fitness Tracker.
class BankAccount:
    def __init__(self, account_holder, balance):
        if balance < 0:
            raise ValueError("Starting balance must be nonnegative.")
        self.account_holder = account_holder
        self.balance = balance
        self.transaction_history = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive.")
        self.balance += amount
        self.transaction_history.append(("deposit", amount))

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive.")
        if amount > self.balance:
            return False
        self.balance -= amount
        self.transaction_history.append(("withdrawal", amount))
        return True

    def get_balance(self):
        return self.balance

    def display_info(self):
        print(f"{self.account_holder}: {self.balance:.2f}")


class Student:
    def __init__(self, name, age, grade, favorite_subject):
        self.name = name
        self.age = age
        self.grade = grade
        self.favorite_subject = favorite_subject


class WorkoutSession:
    total_sessions = 0

    def __init__(self, date, exercise_type, duration, calories_burned):
        if duration <= 0 or calories_burned < 0:
            raise ValueError("Duration must be positive and calories nonnegative.")
        self.date = date
        self.exercise_type = exercise_type
        self.duration = duration
        self.calories_burned = calories_burned
        WorkoutSession.total_sessions += 1

    def calories_per_minute(self):
        return self.calories_burned / self.duration

    def extend_workout(self, extra_minutes, extra_calories):
        if extra_minutes <= 0 or extra_calories < 0:
            raise ValueError("Added minutes must be positive and calories nonnegative.")
        self.duration += extra_minutes
        self.calories_burned += extra_calories

    @classmethod
    def get_total_sessions(cls):
        return cls.total_sessions


# Homework 1: Assistant request data.
class Request(TypedDict, total=False):
    user: str
    message: str
    priority: str


def count_requests(requests: list[Request]) -> int:
    return len(requests)


def get_unique_users(requests: list[Request]) -> list[str]:
    return list(dict.fromkeys(request["user"] for request in requests if "user" in request))


def get_high_priority_requests(requests: list[Request]) -> list[Request]:
    return [request for request in requests if request.get("priority") == "high"]


def format_request(request: Request) -> str:
    priority = request.get("priority", "normal").upper()
    user = request.get("user", "Unknown user")
    message = request.get("message", "(no message)")
    return f"[{priority}] {user}: {message}"


def count_requests_by_priority(requests: list[Request]) -> dict[str, int]:
    return dict(Counter(request.get("priority", "normal") for request in requests))


def search_requests(requests: list[Request], keyword: str) -> list[Request]:
    return [request for request in requests if keyword.casefold() in request.get("message", "").casefold()]


def sort_requests_by_priority(requests: list[Request]) -> list[Request]:
    order = {"high": 0, "normal": 1, "low": 2}
    return sorted(requests, key=lambda request: order.get(request.get("priority", "normal"), 3))


# Homework 2–3: Messages and conversation history.
class Message:
    ALLOWED_ROLES = {"system", "user", "assistant"}

    def __init__(self, role, content):
        role = role.strip().lower()
        if role not in self.ALLOWED_ROLES:
            raise ValueError(f"Unsupported role: {role}")
        self.role = role
        self.content = content
        self.created_at = datetime.now(timezone.utc)

    def display(self):
        return f"{self.role.upper()}: {self.content}"

    def word_count(self):
        return len(self.content.split())

    def is_empty(self):
        return not self.content.strip()

    def contains_keyword(self, keyword):
        return keyword.casefold() in self.content.casefold()

    def __str__(self):
        return self.display()


class Conversation:
    def __init__(self, max_messages=None):
        if max_messages is not None and max_messages < 1:
            raise ValueError("History limit must be positive.")
        self.messages = []
        self.max_messages = max_messages

    def add_message(self, message):
        if not isinstance(message, Message):
            raise TypeError("Expected a Message.")
        self.messages.append(message)
        if self.max_messages is not None and len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def message_count(self):
        return len(self.messages)

    def transcript(self):
        return "\n".join(message.display() for message in self.messages)

    def latest_message(self):
        return self.messages[-1] if self.messages else None

    def count_by_role(self, role):
        return len(self.get_messages_by_role(role))

    def get_messages_by_role(self, role):
        role = role.strip().lower()
        return [message for message in self.messages if message.role == role]

    def clear(self):
        self.messages.clear()


# Homework 4: Local tools with a shared run() interface.
@dataclass
class ToolResult:
    text: str
    success: bool = True


class Tool:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def run(self, input_text):
        raise NotImplementedError("Each tool must implement run().")


class CalculatorTool(Tool):
    def __init__(self):
        super().__init__("calculator", "Evaluate a two-integer expression.")

    def run(self, input_text):
        match = re.fullmatch(r"\s*([+-]?[0-9]+)\s*([+*/-])\s*([+-]?[0-9]+)\s*", input_text)
        if not match:
            return "Error: Enter two integers with an operator (+, -, *, /)."
        left, operator, right = match.groups()
        try:
            a, b = int(left), int(right)
            if operator == "+":
                return str(a + b)
            if operator == "-":
                return str(a - b)
            if operator == "*":
                return str(a * b)
            return str(a / b)
        except ZeroDivisionError:
            return "Error: Division by zero."
        except (ValueError, OverflowError):
            return "Error: Number is too large."


class TextStatisticsTool(Tool):
    def __init__(self):
        super().__init__("statistics", "Count characters and whitespace-delimited words.")

    def run(self, input_text):
        return {"characters": len(input_text), "words": len(input_text.split())}


class MockWeatherTool(Tool):
    def __init__(self):
        super().__init__("weather", "Look up fictional weather for Aarhus.")

    def run(self, input_text):
        if input_text.strip().casefold() == "aarhus":
            return ToolResult("Aarhus: cloudy, 12°C (mock)")
        return ToolResult("No mock weather for that city.", success=False)


# Homework 5: Rule-based routing and conversation state.
class SimpleAssistant:
    HELP = "Try 'calculate 8 + 12', 'count words in some text', 'history', or 'help'."

    def __init__(self, tools):
        self.tools = tools
        self.conversation = Conversation()

    def get_tool(self, name):
        return next((tool for tool in self.tools if tool.name == name), None)

    def respond(self, user_input):
        command = user_input.strip()
        previous_transcript = self.conversation.transcript() if command.casefold() == "history" else ""
        self.conversation.add_message(Message("user", user_input))
        response = self._route(command, previous_transcript)
        self.conversation.add_message(Message("assistant", response))
        return response

    def _route(self, command, previous_transcript):
        normalized = command.casefold()
        if normalized == "history":
            return previous_transcript or "No previous messages."
        if normalized.startswith(("calculate ", "calc ")):
            calculator = self.get_tool("calculator")
            if calculator is None:
                return "Calculator is unavailable."
            expression = command.split(maxsplit=1)[1]
            return f"Calculator result: {calculator.run(expression)}"
        prefix = "count words in "
        if normalized.startswith(prefix):
            statistics = self.get_tool("statistics")
            if statistics is None:
                return "Text statistics are unavailable."
            counts = statistics.run(command[len(prefix):])
            return f"Word count: {counts['words']}"
        return self.HELP


# Homework reflection
# 1. A class defines behavior and attributes. An object is a particular
#    instance with its own state, such as a Task with its own done flag.
# 2. Composition lets Conversation hold Message objects and lets an assistant
#    use interchangeable tools without implementing every tool itself.
# 3. Inheritance gives tools common names, descriptions, and a run() interface
#    while each subclass supplies its own behavior.
# 4. eval() may execute arbitrary Python from user input. The calculator
#    accepts a restricted expression and calls only explicit operations.
# 5. An LLM could translate natural language into a validated tool name and
#    structured arguments. Python would validate and execute the request.


def run_checks():
    for label, value in (("name", name), ("date_of_birth", date_of_birth),
                         ("age", age), ("is_paid_member", is_paid_member),
                         ("membership_price", membership_price)):
        print(f"{label}: {type(value).__name__}")

    tasks = [
        {"name": "read paper", "priority": 2, "done": False},
        {"name": "write code", "priority": 1, "done": False},
        {"name": "email advisor", "priority": 3, "done": True},
        {"name": "prepare slides", "priority": 1, "done": False},
    ]

    # Self-check
    assert isinstance(name, str), "name should be a string"
    assert isinstance(date_of_birth, str), "date_of_birth should be a string"
    assert isinstance(age, int) and not isinstance(age, bool), "age should be an int"
    assert isinstance(is_paid_member, bool), "is_paid_member should be a bool"
    assert isinstance(membership_price, float), "membership_price should be a float"
    print("A0 passed! You correctly used str, int, bool, and float.")


    # Self-check — run this cell
    assert classify_temperature(-5) == "freezing"
    assert classify_temperature(10) == "cold"
    assert classify_temperature(20) == "mild"
    assert classify_temperature(30) == "hot"
    assert classify_temperature(0) == "freezing"
    assert classify_temperature(15) == "cold"
    print("A1 passed!")


    # Self-check
    assert build_greeting("Silvia", role="data steward", city="Aarhus") == \
        "Hello, Silvia! (role: data steward, city: Aarhus)"
    assert build_greeting("Azim") == "Hello, Azim!"
    assert build_greeting("Azim", greeting="Hi") == "Hi, Azim!"
    print("A2 passed!")


    # Self-check
    result = pending_tasks_by_priority(tasks)
    assert result == ["write code", "prepare slides", "read paper"], result
    print("A3 passed!")


    # Self-check
    result = count_by_priority(tasks)
    assert result == {2: 1, 1: 2, 3: 1}, result
    print("A4 passed!")


    # Self-check
    assert safe_call(flaky_divide, 10, 2) == 5.0
    assert safe_call(flaky_divide, 10, 0) == "error: division by zero"
    assert safe_call(flaky_divide, 10, "a") == "error: TypeError"
    print("A5 passed!")


    # Self-check
    t = Task("write code", 1)
    assert t.name == "write code"
    assert t.priority == 1
    assert t.done is False
    assert str(t) == "[ ] write code (priority 1)"
    t.mark_done()
    assert t.done is True
    assert str(t) == "[x] write code (priority 1)"
    print("B1 passed!")


    # Self-check
    Task.total_created = 0  # reset for a clean test
    t1 = Task("a", 1)
    t2 = Task("b", 2)
    t3 = Task("c", 3)
    assert Task.total_created == 3
    assert t1.total_created == 3  # accessible from an instance too
    print("B2 passed!")


    # Self-check
    tl = TaskList()
    tl.add(Task("write code", 1))
    tl.add(Task("read paper", 2))
    tl.add(Task("email advisor", 3))
    assert len(tl) == 3
    pending_names = [t.name for t in tl.pending()]
    assert pending_names == ["write code", "read paper", "email advisor"]
    tl.tasks[2].mark_done()
    pending_names = [t.name for t in tl.pending()]
    assert pending_names == ["write code", "read paper"]
    print("B3 passed!")


    # Self-check
    tl = TaskList()
    tl.add(Task("write code", 1))
    tl.add(Task("read paper", 2))
    agent = SimpleAgent("Agent Smith", tl)

    r1 = agent.act()
    assert r1 == "Agent Smith: working on 'write code'", r1
    r2 = agent.act()
    assert r2 == "Agent Smith: working on 'read paper'", r2
    r3 = agent.act()
    assert r3 == "Agent Smith: nothing to do!", r3
    print("B4 passed! You just built your first (extremely simple) agent.")


    assert count_by_priority_comprehension(tasks) == count_by_priority(tasks)

    account = BankAccount("Sam", 100)
    account.deposit(50)
    assert account.withdraw(30)
    assert not account.withdraw(121)
    assert account.get_balance() == 120
    assert account.transaction_history == [("deposit", 50), ("withdrawal", 30)]
    account.display_info()

    student = Student("Ada", 17, "11th", "Math")
    assert (student.name, student.age, student.grade, student.favorite_subject) == (
        "Ada", 17, "11th", "Math"
    )

    previous_count = WorkoutSession.get_total_sessions()
    workout = WorkoutSession("2026-09-09", "Cycling", 30, 240)
    WorkoutSession("2026-09-10", "Walking", 20, 80)
    assert WorkoutSession.get_total_sessions() == previous_count + 2
    assert workout.calories_per_minute() == 8
    workout.extend_workout(10, 60)
    assert workout.duration == 40 and workout.calories_burned == 300
    assert workout.calories_per_minute() == 7.5

    requests: list[Request] = [
        {"user": "Ada", "message": "What is Python?", "priority": "normal"},
        {"user": "Grace", "message": "Help! My code crashes.", "priority": "high"},
        {"user": "Ada", "message": "Explain classes.", "priority": "normal"},
        {"user": "Linus", "message": "What is a list?", "priority": "low"},
    ]
    assert count_requests(requests) == 4
    assert get_unique_users(requests + [{}]) == ["Ada", "Grace", "Linus"]
    assert get_high_priority_requests(requests + [{}]) == [requests[1]]
    assert format_request(requests[1]) == "[HIGH] Grace: Help! My code crashes."
    assert format_request({}) == "[NORMAL] Unknown user: (no message)"
    assert count_requests_by_priority(requests) == {"normal": 2, "high": 1, "low": 1}
    assert search_requests(requests, "PYTHON") == [requests[0]]
    assert sort_requests_by_priority(requests) == [requests[1], requests[0], requests[2], requests[3]]

    message = Message(" USER ", "Hello world")
    assert message.word_count() == 2 and not message.is_empty()
    assert message.contains_keyword("WORLD") and str(message) == "USER: Hello world"
    assert Message("user", "  ").is_empty()
    try:
        Message("developer", "Hello")
    except ValueError:
        pass
    else:
        raise AssertionError("Unsupported roles must be rejected.")

    conversation = Conversation(max_messages=2)
    assert conversation.latest_message() is None
    conversation.add_message(message)
    assert conversation.message_count() == 1
    conversation.add_message(Message("assistant", "Hi"))
    last = Message("user", "Again")
    conversation.add_message(last)
    assert conversation.message_count() == 2 and conversation.latest_message() is last
    assert conversation.count_by_role("USER") == 1
    assert conversation.get_messages_by_role("user") == [last]
    assert conversation.transcript() == "ASSISTANT: Hi\nUSER: Again"
    try:
        conversation.add_message("plain text")
    except TypeError:
        pass
    else:
        raise AssertionError("Conversation must reject non-Message objects.")
    conversation.clear()
    assert conversation.transcript() == ""

    calculator = CalculatorTool()
    statistics = TextStatisticsTool()
    assert calculator.run("2 + 3") == "5"
    assert calculator.run("7 - -2") == "9"
    assert calculator.run("3 * 4") == "12"
    assert calculator.run("8 / 2") == "4.0"
    assert "Error" in calculator.run("not valid")
    assert "Error" in calculator.run("4 / 0")
    assert statistics.run("Python is useful for AI apps") == {"characters": 28, "words": 6}
    assert MockWeatherTool().run("Aarhus").success
    assert not MockWeatherTool().run("Odense").success

    assistant = SimpleAssistant([calculator, statistics])
    assert assistant.get_tool("missing") is None
    assert assistant.respond("calculate 10 + 5") == "Calculator result: 15"
    assert assistant.respond("CALC 8 + 12") == "Calculator result: 20"
    assert assistant.respond("count words in Agentic systems use tools") == "Word count: 4"
    assert assistant.respond("Hello there") == assistant.HELP
    assert assistant.respond("help") == assistant.HELP
    assert assistant.conversation.message_count() == 10
    assert "USER: calculate 10 + 5" in assistant.respond("history")
    assert assistant.conversation.latest_message().role == "assistant"
    print("All Session 1 checks passed.")


if __name__ == "__main__":
    run_checks()
