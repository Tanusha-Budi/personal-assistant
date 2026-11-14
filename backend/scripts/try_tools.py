from app.tools.langchain_tools import get_calendar_events

print("NAME:", get_calendar_events.name)
print("DESCRIPTION:", get_calendar_events.description)
print("ARGS:", get_calendar_events.args)
print("RESULT:", get_calendar_events.invoke({"day": "2026-11-14"}))