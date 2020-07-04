class Commit:
    commit_id = ""
    parent_commits = []

    def __init__(self, commit_id, parent_commits):
        if not commit_id:
            raise ValueError("empty commit id")
        self.commit_id = commit_id
        self.parentCommitID = parent_commits
