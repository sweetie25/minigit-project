from ..repository import repo_find
from ..refs import ref_list, show_ref

def cmd_show_ref(args):
    """
    Handle `minigit show-ref`
    """
    repo = repo_find()
    refs = ref_list(repo)
    show_ref(repo, refs)
