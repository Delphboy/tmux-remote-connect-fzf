import os
import json
from typing import Optional, List


class Session:
    def __init__(
        self,
        session: str,
        command: str = "tmux new-session -A -s",
        server: str = "",
    ):
        self.command = command
        self.session = session
        self.server = server
        self.is_local = self.server == ""

    def __str__(self):
        prefix = "Local" if self.is_local else f"{self.server}"
        return f"{prefix}: {self.session}"

    def get_connection_command(self):
        if self.is_local:
            return f"{self.command} {self.session}"
        else:
            return f"{self.command} -t 'tmux new-session -A -s {self.session}'"


def get_config() -> Optional[dict]:
    config_file_name = "config.json"
    config = None

    if not os.path.exists(config_file_name):
        return None

    with open(config_file_name) as f:
        config = json.load(f)
    return config


def build_local_list() -> List[Session]:
    local_sessions = os.popen("tmux ls").read().split("\n")
    local_sessions = [Session(s.split(":")[0]) for s in local_sessions[:-1]]
    return local_sessions


def build_global_list() -> Optional[List[Session]]:
    config = get_config()
    if config is None:
        return []

    global_sessions = []
    for k in list(config.keys()):
        server = k
        command = config[k]["ssh_connection"]
        sessions = config[k]["session_names"]
        for session in sessions:
            global_sessions.append(Session(session, command, server))

    return global_sessions


def get_session(selection: str, sessions: List[Session]) -> Session:
    server, selection = selection.split(":")
    server = sanitise(server)
    server = "" if server == "Local" else server
    selection = sanitise(selection)

    for s in sessions:
        if (s.session == selection) and (s.server == server):
            return s
    raise Exception("Session not found")


def fzf_er(sessions: List[Session]) -> str:
    return "".join([str(s) + "\n" for s in sessions])[:-1]


def sanitise(s: str) -> str:
    return s.replace("\n", "").strip()


if __name__ == "__main__":
    local_sessions = build_local_list()
    global_sessions = build_global_list()
    all_sessions = local_sessions + global_sessions

    selection = os.popen(f"echo '{fzf_er(all_sessions)}' | fzf").read()
    session = get_session(selection, all_sessions)
    print(session.get_connection_command())
