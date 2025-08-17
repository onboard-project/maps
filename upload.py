import os
import git # pip install GitPython
import math
import sys

def get_all_files(source_folder):
    """
    Reads all file paths from the given folder and its subfolders.
    """
    if not os.path.isdir(source_folder):
        print(f"Error: Source folder '{source_folder}' does not exist or is not a directory.")
        sys.exit(1)

    all_files = []
    print(f"Scanning files in '{source_folder}'...")
    for root, _, files in os.walk(source_folder):
        for filename in files:
            full_path = os.path.join(root, filename)
            # Add relative path to the repo's root (important for git add)
            # We will later need to make sure the repo is initialized at a suitable base path
            all_files.append(os.path.abspath(full_path)) 
    print(f"Found {len(all_files)} files.")
    return all_files

def initialize_git_repo(repo_path, remote_url):
    """
    Initializes a Git repository or loads an existing one,
    and ensures a remote 'origin' is configured.
    """
    try:
        if os.path.exists(os.path.join(repo_path, '.git')):
            print(f"Loading existing Git repository at '{repo_path}'...")
            repo = git.Repo(repo_path)
            if repo.is_dirty(untracked_files=True):
                print("Warning: Repository has untracked files or uncommitted changes. Please commit or stash them before proceeding.")
                # You might want to exit here or add an option to force
                # sys.exit(1)
        else:
            print(f"Initializing new Git repository at '{repo_path}'...")
            os.makedirs(repo_path, exist_ok=True)
            repo = git.Repo.init(repo_path)
            print("Repository initialized.")

        # Check and set up remote 'origin'
        try:
            origin = repo.remote('origin')
            if origin.url != remote_url:
                print(f"Updating remote 'origin' URL from '{origin.url}' to '{remote_url}'")
                origin.set_url(remote_url)
        except git.exc.GitCommandError:
            print(f"Adding remote 'origin' with URL: '{remote_url}'")
            repo.create_remote('origin', remote_url)
        
        # Ensure the repo is on a branch for pushing
        if not repo.head.is_valid():
            print("Repository has no commits yet. Creating initial commit and 'master' branch.")
            # Create an empty initial commit if needed, so there's a branch to push to
            repo.index.commit("Initial repository setup")
            # If no branch exists, GitPython might not automatically create one on first push.
            # This ensures there's at least a 'master' or 'main' branch to push to.
            # However, typically the first `git add` and `git commit` will establish the master branch.
            # The following might be redundant if the first real commit creates the branch.
            if 'master' not in repo.branches and 'main' not in repo.branches:
                try:
                    repo.head.reference = repo.create_head('main')
                    repo.head.reset(index=True, working_tree=True)
                except Exception as e:
                    print(f"Could not create 'main' branch, trying 'master': {e}")
                    try:
                        repo.head.reference = repo.create_head('master')
                        repo.head.reset(index=True, working_tree=True)
                    except Exception as e:
                        print(f"Could not create 'master' branch either. Please ensure your repository is on a branch: {e}")
                        sys.exit(1)


        return repo
    except git.exc.InvalidGitRepositoryError:
        print(f"Error: '{repo_path}' is not a valid Git repository.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during Git repository initialization: {e}")
        sys.exit(1)

def add_commit_push_chunk(repo, files_chunk, commit_message, chunk_num, total_chunks, base_repo_path):
    """
    Adds a chunk of files, commits them, and pushes to the remote repository.
    """
    if not files_chunk:
        print("Skipping empty chunk.")
        return

    print(f"\n--- Processing Chunk {chunk_num}/{total_chunks} ({len(files_chunk)} files) ---")

    # Convert absolute paths to paths relative to the repository's root
    relative_files_to_add = []
    for f_path in files_chunk:
        try:
            rel_path = os.path.relpath(f_path, base_repo_path)
            relative_files_to_add.append(rel_path)
        except ValueError as e:
            print(f"Warning: Could not get relative path for '{f_path}' from '{base_repo_path}'. Skipping. Error: {e}")
            continue # Skip files that cannot be made relative

    if not relative_files_to_add:
        print("No valid files to add in this chunk after path conversion. Skipping.")
        return

    try:
        print("Adding files to staging area...")
        repo.index.add(relative_files_to_add)
        print("Files added. Committing...")
        repo.index.commit(commit_message)
        print(f"Commit successful: '{commit_message}'")

        print("Pushing to remote repository...")
        # Get the current branch
        current_branch = repo.active_branch
        # Push to the remote 'origin'
        repo.remote('origin').push(refspec=f'{current_branch.name}:{current_branch.name}')
        print("Push successful.")

    except git.exc.GitCommandError as e:
        print(f"Git Command Error: {e}")
        print("Attempting to revert staged changes due to error...")
        try:
            repo.index.reset(index=True, working_tree=False) # Unstage all
            print("Staged changes reverted.")
        except Exception as reset_e:
            print(f"Error reverting staged changes: {reset_e}")
        print("Please resolve the issue (e.g., authentication, conflicting changes) and try again.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during commit/push: {e}")
        sys.exit(1)

def main():
    source_folder = input("Enter the path to the source folder (e.g., /path/to/my_data): ").strip()
    repo_path = input("Enter the path to the Git repository (where .git folder is or will be created): ").strip()
    remote_url = input("Enter the remote Git repository URL (e.g., https://github.com/user/repo.git): ").strip()
    chunk_size = 6000 # Default chunk size
    
    # Optional: allow user to set chunk size
    try:
        user_chunk = input(f"Enter chunk size (default is {chunk_size}, enter to use default): ").strip()
        if user_chunk:
            chunk_size = int(user_chunk)
            if chunk_size <= 0:
                raise ValueError("Chunk size must be positive.")
    except ValueError as e:
        print(f"Invalid chunk size: {e}. Using default {chunk_size}.")


    all_files = get_all_files(source_folder)

    if not all_files:
        print("No files found to process. Exiting.")
        sys.exit(0)

    repo = initialize_git_repo(repo_path, remote_url)

    total_files = len(all_files)
    total_chunks = math.ceil(total_files / chunk_size)

    print(f"\nStarting file processing in {total_chunks} chunks of {chunk_size} files.")

    # Get initial branch name for first push
    current_branch_name = repo.active_branch.name
    print(f"Working on branch: {current_branch_name}")


    for i in range(0, total_files, chunk_size):
        chunk_num = (i // chunk_size) + 1
        files_chunk = all_files[i:i + chunk_size]
        commit_message = f"Add files from chunk {chunk_num}/{total_chunks} (Source: {os.path.basename(source_folder)})"
        
        add_commit_push_chunk(repo, files_chunk, commit_message, chunk_num, total_chunks, repo_path)
    
    print("\nAll files processed, committed, and pushed successfully!")

if __name__ == "__main__":
    main()