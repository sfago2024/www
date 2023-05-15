import logging
import shutil
from datetime import date, datetime, time
from pathlib import Path
from textwrap import dedent

from .event import Database, Session, Speaker

logger = logging.getLogger(__name__)


def render_page(title: str, content: str):
    date = datetime.now()
    return dedent(
        """\
        <!DOCTYPE html>
        <html lang="en-us">
        <head>
          <meta charset="utf-8">
          <title>{title} — AGO 2024 San Francisco</title>
          <meta name="viewport" content="width=device-width,initial-scale=1">
          <link rel="stylesheet" href="/default.css">
        </head>
        <body>
          <div class="main-flex">
            <header>
              <div>
                <img src="/img/logo.png" alt="AGO 2024 San Francisco logo">
                <div class="line"></div>
                <p class="dates"><time datetime="2024-06-30">June 30</time> – <time datetime="2024-07-04">July 4, 2024</time></p>
              </div>
            </header>
            <nav>
              <a href="/schedule.html">Schedule</a>
              <a href="/sessions.html">Sessions</a>
              <a href="/speakers.html">Speakers</a>
            </nav>
            <div class="content">

        {content}

            </div>
            <div class="spacer"></div>
            <footer>
              <p>This page was last updated on {date:%A, %B %d, %Y, at %I:%M %p}.</p>
            </footer>
          </div>
        </body>
        </html>
        """
    ).format(**locals())


def speaker_page(speaker: Speaker, database: Database) -> str:
    if stubs := speaker.data.presenter_at:
        sessions = "<ul>"
        for stub in stubs:
            if session := database.sessions.get(stub):
                sessions += f"<li>{session.link}</li>"
            else:
                sessions += f"<li>(unknown session with identifier {stub})</li>"
    else:
        sessions = "<p>None yet</p>"
    content = dedent(
        """\
        <h1>{speaker.data.speaker_display_name}</h1>
        <h2>Biography</h2>
        <p>{speaker.data.speaker_biography}</p>
        <h2>Sessions</h2>
        {sessions}
        """
    ).format(**locals())
    return render_page(title=f"{speaker.data.speaker_display_name}", content=content)


def session_page(session: Session, database: Database) -> str:
    if stubs := session.data.speakers:
        speakers = "<ul>"
        for stub in stubs:
            if speaker := database.speakers.get(stub):
                speakers += f"<li>{speaker.link}</li>"
            else:
                speakers += f"<li>(unknown speaker with identifier {stub})</li>"
    else:
        speakers = "<p>None yet</p>"
    content = dedent(
        """\
        <h1>{session.data.session_name}</h1>
        <h2>Date/Time</h2>
        <p>{session.data.session_start_date_time:%A, %B %d, %Y}<br>
        {session.data.session_start_date_time:%I:%M %p} – {session.data.session_end_date_time:%I:%M %p} ({session.data.timezone_name})</p>
        <h2>Location</h2>
        (not implemented yet)
        <h2>Description</h2>
        {session.data.session_description}
        <h2>Speakers</h2>
        {speakers}
        """
    ).format(**locals())
    return render_page(title=f"{session.data.session_name}", content=content)


def index_page(title: str, links: list[str]) -> str:
    items = "\n".join(f"<li>{link}</li>" for link in sorted(links))
    content = dedent(
        """
        <h1>{title}</h1>
        <ul>
        {items}
        </ul>
        """
    ).format(**locals())
    return render_page(title, content)


def schedule_page(title: str, database: Database) -> str:
    days: dict[date, dict[time, list[str]]] = {}
    for session in database.sessions.values():
        start = session.data.session_start_date_time
        times = days.setdefault(start.date(), {})
        links = times.setdefault(start.time(), [])
        links.append(session.link)

    lines = []
    for date, times in sorted(days.items()):
        lines.append(f"<h2>{date}</h2>")
        for time, links in sorted(times.items()):
            lines.append(f"<h3>{time}</h3>")
            lines.append(f"<ul>")
            for link in links:
                lines.append(f"<li>{link}</li>")
            lines.append(f"</ul>")

    joined_lines = "\n".join(lines)
    content = dedent(
        """
        <h1>Schedule</h1>
        {joined_lines}
        """
    ).format(**locals())
    return render_page(title, content)


def generate_pages(database: Database, static_dir: Path, output_dir: Path) -> None:
    shutil.rmtree(output_dir)
    (output_dir).mkdir(exist_ok=True)
    shutil.copytree(static_dir, output_dir, dirs_exist_ok=True)

    (output_dir / "schedule.html").write_text(schedule_page("Schedule", database))

    (output_dir / "sessions").mkdir()
    links = []
    for session in database.sessions.values():
        page = session_page(session, database)
        path = Path(session.url).relative_to("/")
        (output_dir / path).write_text(page)
        links.append(session.link)
    (output_dir / "sessions.html").write_text(index_page("Sessions", links))

    (output_dir / "speakers").mkdir()
    links = []
    for speaker in database.speakers.values():
        page = speaker_page(speaker, database)
        path = Path(speaker.url).relative_to("/")
        (output_dir / path).write_text(page)
        links.append(speaker.link)
    (output_dir / "speakers.html").write_text(index_page("Speakers", links))
