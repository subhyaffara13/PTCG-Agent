import subprocess
import sys

def test_with_missing_lzma_runtime():
    """Tests if ModuleNotFoundError is hit when calling lzma without
    having the module available.
    """
    code = textwrap.dedent(
        """
        import sys
        import pytest
        sys.modules['lzma'] = None
        import pandas as pd
        df = pd.DataFrame()
        with pytest.raises(ModuleNotFoundError, match='import of lzma'):
            df.to_csv('foo.csv', compression='xz')
        """
    )
    subprocess.check_output([sys.executable, "-c", code], stderr=subprocess.PIPE)

