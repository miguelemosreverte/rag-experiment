# Git Operations Tool

## Description
Performs Git version control operations on local repositories. Supports status checks, commits, branching, merging, and history inspection. All operations are non-destructive by default — force operations require explicit confirmation.

## Parameters
- `repo_path` (required): Path to the Git repository root.
- `operation` (required): The Git operation to perform.

## Operations

### Status
```python
status = git_op(repo_path="/projects/myapp", operation="status")
# Returns: {"branch": "feature/auth", "staged": [...], "modified": [...], "untracked": [...]}
```

### Commit
```python
git_op(repo_path="/projects/myapp", operation="commit",
       message="Add OAuth2 login flow", files=["src/auth.py", "tests/test_auth.py"])
```

### Branch
```python
git_op(repo_path="/projects/myapp", operation="create_branch", branch_name="feature/payments")
git_op(repo_path="/projects/myapp", operation="switch_branch", branch_name="main")
git_op(repo_path="/projects/myapp", operation="list_branches")
```

### Log
```python
log = git_op(repo_path="/projects/myapp", operation="log", count=10)
# Returns: [{"hash": "abc123", "author": "...", "date": "...", "message": "..."}]
```

### Diff
```python
diff = git_op(repo_path="/projects/myapp", operation="diff", ref="HEAD~3")
```

### Merge
```python
git_op(repo_path="/projects/myapp", operation="merge", branch_name="feature/auth")
```

## Safety
- No force-push or hard reset without explicit `force=True`
- Uncommitted changes are stashed automatically before branch switches
- Merge conflicts are reported but never auto-resolved
- All destructive operations create a backup ref (`refs/backup/<timestamp>`)

## Hooks
Pre-commit hooks are respected. If a hook fails, the commit is aborted and the hook output is returned.
