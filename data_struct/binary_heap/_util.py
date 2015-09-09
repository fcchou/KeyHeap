def _get_parent(heap, idx):
    """Get the parent index-value of the input index."""
    idx_parent = (idx - 1) // 2
    val_parent = heap._idx2val(idx_parent) if idx != 0 else None
    return idx_parent, val_parent


def _get_children(heap, idx):
    """Get the children index-value of the input index."""
    length = len(heap)
    idx_left = 2 * idx + 1
    val_left = heap._idx2val(idx_left) if idx_left < length else None
    idx_right = idx_left + 1
    val_right = heap._idx2val(idx_right) if idx_right < length else None
    return idx_left, val_left, idx_right, val_right


def down_heap(heap, idx):
    """Perform down-heap operation on input index."""
    idx_curr = idx
    val_curr = heap._idx2val(idx)
    while True:
        idx_left, val_left, idx_right, val_right = (
            _get_children(heap, idx_curr))
        if val_left is None:
            break
        elif val_right is None or heap._upper_eq(val_left, val_right):
            child_idx_upper = idx_left
            child_val_upper = val_left
        else:
            child_idx_upper = idx_right
            child_val_upper = val_right

        if heap._upper_eq(val_curr, child_val_upper):
            break
        heap._swap(idx_curr, child_idx_upper)
        idx_curr = child_idx_upper


def up_heap(heap, idx):
    """Perform up-heap operation on input index."""
    idx_curr = idx
    val_curr = heap._idx2val(idx)
    while True:
        idx_parent, val_parent = _get_parent(heap, idx_curr)
        if val_parent is None or heap._upper_eq(val_parent, val_curr):
            break
        heap._swap(idx_curr, idx_parent)
        idx_curr = idx_parent
