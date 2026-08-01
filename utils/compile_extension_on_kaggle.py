
def compile_extension_on_kaggle(configuration=None):
    """Compiles the C++ ptcg_core extension on Kaggle at module load time or Step 0."""
    import sys
    import os
    import shutil
    import subprocess
    from pathlib import Path
    
    # 1. Check if we are running on Kaggle
    is_kaggle_run = any(k.startswith("KAGGLE") for k in os.environ) or not os.path.exists("build_submission.py")
    if not is_kaggle_run:
        return False

    sys.stderr.write("[compile] Running inside Kaggle sandbox. Checking C++ extension...\n")
        
    # 2. Check if we have already built the .so file in /kaggle/working
    working_dir = Path("/kaggle/working")
    if not working_dir.exists():
        sys.stderr.write("[compile] /kaggle/working does not exist. Skipping compilation.\n")
        return False
        
    # See if ptcg_core*.so is already in /kaggle/working
    so_files = list(working_dir.glob("ptcg_core*.so"))
    if so_files:
        sys.stderr.write(f"[compile] Found pre-compiled C++ extension: {so_files[0].name}. Adding to path.\n")
        if str(working_dir) not in sys.path:
            sys.path.insert(0, str(working_dir))
        try:
            import ptcg_core  # type: ignore
            _update_mcts_module(ptcg_core)
        except Exception as e:
            sys.stderr.write(f"[compile] Error loading pre-compiled extension: {e}\n")
        return True
        
    # 3. Locate source files in the agent extraction directory
    raw_path = None
    if isinstance(configuration, dict):
        raw_path = configuration.get("__raw_path__")
    
    if not raw_path:
        # Fallback to sys.path or guess
        sys.stderr.write("[compile] __raw_path__ not found in configuration. Trying path lookup...\n")
        for p in sys.path:
            if p and Path(p).joinpath("setup.py").exists():
                raw_path = str(Path(p).joinpath("main.py"))
                break
                
    if not raw_path:
        # Try parent directory relative guess
        curr_dir = Path(__file__).parent.resolve() if "__file__" in globals() and globals()["__file__"] else Path(os.getcwd())
        if curr_dir.joinpath("setup.py").exists():
            raw_path = str(curr_dir.joinpath("main.py"))
            
    if not raw_path:
        sys.stderr.write("[compile] Could not determine agent extraction directory. Skipping compilation.\n")
        return False
        
    curr_agent_dir = Path(raw_path).parent.resolve()
    src_dir = curr_agent_dir / "src"
    setup_file = curr_agent_dir / "setup.py"
    
    sys.stderr.write(f"[compile] Resolved agent extraction directory: {curr_agent_dir}\n")
    
    if not src_dir.exists() or not setup_file.exists():
        sys.stderr.write("[compile] C++ source files or setup.py not found in agent directory. Skipping on-the-fly compile.\n")
        return False
        
    # 4. Create temporary build dir in /kaggle/working
    build_dir = working_dir / "ptcg_build"
    try:
        if build_dir.exists():
            shutil.rmtree(build_dir, ignore_errors=True)
        build_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy src/ and setup.py to build_dir
        shutil.copytree(src_dir, build_dir / "src")
        shutil.copy2(setup_file, build_dir / "setup.py")
        if (curr_agent_dir / "CMakeLists.txt").exists():
            shutil.copy2(curr_agent_dir / "CMakeLists.txt", build_dir / "CMakeLists.txt")
            
        sys.stderr.write(f"[compile] Copied C++ sources to build dir: {build_dir}\n")
        
        # 5. Run compilation command
        sys.stderr.write("[compile] Compiling C++ ptcg_core extension on-the-fly...\n")
        res = subprocess.run(
            [sys.executable, "setup.py", "build_ext", "--inplace"],
            cwd=str(build_dir),
            capture_output=True,
            text=True
        )
        sys.stderr.write(f"[compile] Compilation stdout:\n{res.stdout}\n")
        sys.stderr.write(f"[compile] Compilation stderr:\n{res.stderr}\n")
        
        if res.returncode != 0:
            sys.stderr.write(f"[compile] Compilation failed with exit code: {res.returncode}\n")
            return False
            
        # 6. Locate compiled .so file
        compiled_so = list(build_dir.glob("ptcg_core*.so"))
        if not compiled_so:
            sys.stderr.write("[compile] Compilation completed but ptcg_core*.so not found.\n")
            return False
            
        # Copy to /kaggle/working
        target_so = working_dir / compiled_so[0].name
        shutil.copy2(compiled_so[0], target_so)
        sys.stderr.write(f"[compile] Successfully copied compiled extension to {target_so}\n")
        
        # Add to sys.path
        if str(working_dir) not in sys.path:
            sys.path.insert(0, str(working_dir))
            
        # Try importing to verify
        import ptcg_core  # type: ignore
        _update_mcts_module(ptcg_core)
        sys.stderr.write("[compile] ptcg_core successfully compiled, loaded, and verified!\n")
        return True
    except Exception as build_err:
        sys.stderr.write(f"[compile] Exception during on-the-fly compilation: {build_err}\n")
        return False


def compile_extension_on_kaggle(configuration=None):
    """Compiles the C++ ptcg_core extension on Kaggle at module load time or Step 0."""
    import sys
    import os
    import shutil
    import subprocess
    from pathlib import Path
    
    # 1. Check if we are running on Kaggle
    is_kaggle_run = any(k.startswith("KAGGLE") for k in os.environ) or not os.path.exists("build_submission.py")
    if not is_kaggle_run:
        return False

    sys.stderr.write("[compile] Running inside Kaggle sandbox. Checking C++ extension...\n")
        
    # 2. Check writable working directory (fallback to tempdir in competition submission containers)
    import tempfile
    working_dir = Path("/kaggle/working")
    if not working_dir.exists():
        working_dir = Path(tempfile.gettempdir()) / "kaggle_working"
        working_dir.mkdir(parents=True, exist_ok=True)
        
    # See if ptcg_core*.so is already in /kaggle/working
    so_files = list(working_dir.glob("ptcg_core*.so"))
    if so_files:
        sys.stderr.write(f"[compile] Found pre-compiled C++ extension: {so_files[0].name}. Adding to path.\n")
        if str(working_dir) not in sys.path:
            sys.path.insert(0, str(working_dir))
        try:
            import ptcg_core  # type: ignore
            _update_mcts_module(ptcg_core)
        except Exception as e:
            sys.stderr.write(f"[compile] Error loading pre-compiled extension: {e}\n")
        return True
        
    # 3. Locate source files in the agent extraction directory
    raw_path = None
    if isinstance(configuration, dict):
        raw_path = configuration.get("__raw_path__")
    
    if not raw_path:
        # Fallback to sys.path or guess
        sys.stderr.write("[compile] __raw_path__ not found in configuration. Trying path lookup...\n")
        for p in sys.path:
            if p and Path(p).joinpath("setup.py").exists():
                raw_path = str(Path(p).joinpath("main.py"))
                break
                
    if not raw_path:
        # Try parent directory relative guess
        curr_dir = Path(__file__).parent.resolve() if "__file__" in globals() and globals()["__file__"] else Path(os.getcwd())
        if curr_dir.joinpath("setup.py").exists():
            raw_path = str(curr_dir.joinpath("main.py"))
            
    if not raw_path:
        sys.stderr.write("[compile] Could not determine agent extraction directory. Skipping compilation.\n")
        return False
        
    curr_agent_dir = Path(raw_path).parent.resolve()
    src_dir = curr_agent_dir / "src"
    setup_file = curr_agent_dir / "setup.py"
    
    sys.stderr.write(f"[compile] Resolved agent extraction directory: {curr_agent_dir}\n")
    
    if not src_dir.exists() or not setup_file.exists():
        sys.stderr.write("[compile] C++ source files or setup.py not found in agent directory. Skipping on-the-fly compile.\n")
        return False
        
    # 4. Create temporary build dir in /kaggle/working
    build_dir = working_dir / "ptcg_build"
    try:
        if build_dir.exists():
            shutil.rmtree(build_dir, ignore_errors=True)
        build_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy src/ and setup.py to build_dir
        shutil.copytree(src_dir, build_dir / "src")
        shutil.copy2(setup_file, build_dir / "setup.py")
        if (curr_agent_dir / "CMakeLists.txt").exists():
            shutil.copy2(curr_agent_dir / "CMakeLists.txt", build_dir / "CMakeLists.txt")
            
        sys.stderr.write(f"[compile] Copied C++ sources to build dir: {build_dir}\n")
        
        # 5. Run compilation command
        sys.stderr.write("[compile] Compiling C++ ptcg_core extension on-the-fly...\n")
        try:
            res = subprocess.run(
                [sys.executable, "setup.py", "build_ext", "--inplace"],
                cwd=str(build_dir),
                capture_output=True,
                text=True,
                timeout=120
            )
        except subprocess.TimeoutExpired as e:
            sys.stderr.write(f"[compile] Compilation timed out: {e}\n")
            return False
        sys.stderr.write(f"[compile] Compilation stdout:\n{res.stdout}\n")
        sys.stderr.write(f"[compile] Compilation stderr:\n{res.stderr}\n")
        
        if res.returncode != 0:
            sys.stderr.write(f"[compile] Compilation failed with exit code: {res.returncode}\n")
            return False
            
        # 6. Locate compiled .so file
        compiled_so = list(build_dir.glob("ptcg_core*.so"))
        if not compiled_so:
            sys.stderr.write("[compile] Compilation completed but ptcg_core*.so not found.\n")
            return False
            
        # Copy to /kaggle/working
        target_so = working_dir / compiled_so[0].name
        shutil.copy2(compiled_so[0], target_so)
        sys.stderr.write(f"[compile] Successfully copied compiled extension to {target_so}\n")
        
        # Add to sys.path
        if str(working_dir) not in sys.path:
            sys.path.insert(0, str(working_dir))
            
        # Try importing to verify
        import ptcg_core  # type: ignore
        _update_mcts_module(ptcg_core)
        sys.stderr.write("[compile] ptcg_core successfully compiled, loaded, and verified!\n")
        return True
    except Exception as build_err:
        sys.stderr.write(f"[compile] Exception during on-the-fly compilation: {build_err}\n")
        return False


def compile_extension_on_kaggle(configuration=None):
    """Compiles the C++ ptcg_core extension on Kaggle at module load time or Step 0."""
    import sys
    import os
    import shutil
    import subprocess
    from pathlib import Path
    
    # 1. Check if we are running on Kaggle
    is_kaggle_run = any(k.startswith("KAGGLE") for k in os.environ) or not os.path.exists("build_submission.py")
    if not is_kaggle_run:
        return False

    sys.stderr.write("[compile] Running inside Kaggle sandbox. Checking C++ extension...\n")
        
    # 2. Check writable working directory (fallback to tempdir in competition submission containers)
    import tempfile
    working_dir = Path("/kaggle/working")
    if not working_dir.exists():
        working_dir = Path(tempfile.gettempdir()) / "kaggle_working"
        working_dir.mkdir(parents=True, exist_ok=True)
        
    # See if ptcg_core*.so is already in /kaggle/working
    so_files = list(working_dir.glob("ptcg_core*.so"))
    if so_files:
        sys.stderr.write(f"[compile] Found pre-compiled C++ extension: {so_files[0].name}. Adding to path.\n")
        if str(working_dir) not in sys.path:
            sys.path.insert(0, str(working_dir))
        try:
            import ptcg_core  # type: ignore
            _update_mcts_module(ptcg_core)
        except Exception as e:
            sys.stderr.write(f"[compile] Error loading pre-compiled extension: {e}\n")
        return True
        
    # 3. Locate source files in the agent extraction directory
    raw_path = None
    if isinstance(configuration, dict):
        raw_path = configuration.get("__raw_path__")
    
    if not raw_path:
        # Fallback to sys.path or guess
        sys.stderr.write("[compile] __raw_path__ not found in configuration. Trying path lookup...\n")
        for p in sys.path:
            if p and Path(p).joinpath("setup.py").exists():
                raw_path = str(Path(p).joinpath("main.py"))
                break
                
    if not raw_path:
        # Try parent directory relative guess
        curr_dir = Path(__file__).parent.resolve() if "__file__" in globals() and globals()["__file__"] else Path(os.getcwd())
        if curr_dir.joinpath("setup.py").exists():
            raw_path = str(curr_dir.joinpath("main.py"))
            
    if not raw_path:
        sys.stderr.write("[compile] Could not determine agent extraction directory. Skipping compilation.\n")
        return False
        
    curr_agent_dir = Path(raw_path).parent.resolve()
    src_dir = curr_agent_dir / "src"
    setup_file = curr_agent_dir / "setup.py"
    
    sys.stderr.write(f"[compile] Resolved agent extraction directory: {curr_agent_dir}\n")
    
    if not src_dir.exists() or not setup_file.exists():
        sys.stderr.write("[compile] C++ source files or setup.py not found in agent directory. Skipping on-the-fly compile.\n")
        return False
        
    # 4. Create temporary build dir in /kaggle/working
    build_dir = working_dir / "ptcg_build"
    try:
        if build_dir.exists():
            shutil.rmtree(build_dir, ignore_errors=True)
        build_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy src/ and setup.py to build_dir
        shutil.copytree(src_dir, build_dir / "src")
        shutil.copy2(setup_file, build_dir / "setup.py")
        if (curr_agent_dir / "CMakeLists.txt").exists():
            shutil.copy2(curr_agent_dir / "CMakeLists.txt", build_dir / "CMakeLists.txt")
            
        sys.stderr.write(f"[compile] Copied C++ sources to build dir: {build_dir}\n")
        
        # 5. Run compilation command
        sys.stderr.write("[compile] Compiling C++ ptcg_core extension on-the-fly...\n")
        try:
            res = subprocess.run(
                [sys.executable, "setup.py", "build_ext", "--inplace"],
                cwd=str(build_dir),
                capture_output=True,
                text=True,
                timeout=120
            )
        except subprocess.TimeoutExpired as e:
            sys.stderr.write(f"[compile] Compilation timed out: {e}\n")
            return False
        sys.stderr.write(f"[compile] Compilation stdout:\n{res.stdout}\n")
        sys.stderr.write(f"[compile] Compilation stderr:\n{res.stderr}\n")
        
        if res.returncode != 0:
            sys.stderr.write(f"[compile] Compilation failed with exit code: {res.returncode}\n")
            return False
            
        # 6. Locate compiled .so file
        compiled_so = list(build_dir.glob("ptcg_core*.so"))
        if not compiled_so:
            sys.stderr.write("[compile] Compilation completed but ptcg_core*.so not found.\n")
            return False
            
        # Copy to /kaggle/working
        target_so = working_dir / compiled_so[0].name
        shutil.copy2(compiled_so[0], target_so)
        sys.stderr.write(f"[compile] Successfully copied compiled extension to {target_so}\n")
        
        # Add to sys.path
        if str(working_dir) not in sys.path:
            sys.path.insert(0, str(working_dir))
            
        # Try importing to verify
        import ptcg_core  # type: ignore
        _update_mcts_module(ptcg_core)
        sys.stderr.write("[compile] ptcg_core successfully compiled, loaded, and verified!\n")
        return True
    except Exception as build_err:
        sys.stderr.write(f"[compile] Exception during on-the-fly compilation: {build_err}\n")
        return False


def compile_extension_on_kaggle(configuration=None):
    """Compiles the C++ ptcg_core extension on Kaggle at module load time or Step 0."""
    import sys
    import os
    import shutil
    import subprocess
    from pathlib import Path
    
    # 1. Check if we are running on Kaggle
    is_kaggle_run = any(k.startswith("KAGGLE") for k in os.environ) or not os.path.exists("build_submission.py")
    if not is_kaggle_run:
        return False

    sys.stderr.write("[compile] Running inside Kaggle sandbox. Checking C++ extension...\n")
        
    # 2. Check if we have already built the .so file in /kaggle/working
    working_dir = Path("/kaggle/working")
    if not working_dir.exists():
        sys.stderr.write("[compile] /kaggle/working does not exist. Skipping compilation.\n")
        return False
        
    # See if ptcg_core*.so is already in /kaggle/working
    so_files = list(working_dir.glob("ptcg_core*.so"))
    if so_files:
        sys.stderr.write(f"[compile] Found pre-compiled C++ extension: {so_files[0].name}. Adding to path.\n")
        if str(working_dir) not in sys.path:
            sys.path.insert(0, str(working_dir))
        try:
            import ptcg_core  # type: ignore
            _update_mcts_module(ptcg_core)
        except Exception as e:
            sys.stderr.write(f"[compile] Error loading pre-compiled extension: {e}\n")
        return True
        
    # 3. Locate source files in the agent extraction directory
    raw_path = None
    if isinstance(configuration, dict):
        raw_path = configuration.get("__raw_path__")
    
    if not raw_path:
        # Fallback to sys.path or guess
        sys.stderr.write("[compile] __raw_path__ not found in configuration. Trying path lookup...\n")
        for p in sys.path:
            if p and Path(p).joinpath("setup.py").exists():
                raw_path = str(Path(p).joinpath("main.py"))
                break
                
    if not raw_path:
        # Try parent directory relative guess
        curr_dir = Path(__file__).parent.resolve() if "__file__" in globals() and globals()["__file__"] else Path(os.getcwd())
        if curr_dir.joinpath("setup.py").exists():
            raw_path = str(curr_dir.joinpath("main.py"))
            
    if not raw_path:
        sys.stderr.write("[compile] Could not determine agent extraction directory. Skipping compilation.\n")
        return False
        
    curr_agent_dir = Path(raw_path).parent.resolve()
    src_dir = curr_agent_dir / "src"
    setup_file = curr_agent_dir / "setup.py"
    
    sys.stderr.write(f"[compile] Resolved agent extraction directory: {curr_agent_dir}\n")
    
    if not src_dir.exists() or not setup_file.exists():
        sys.stderr.write("[compile] C++ source files or setup.py not found in agent directory. Skipping on-the-fly compile.\n")
        return False
        
    # 4. Create temporary build dir in /kaggle/working
    build_dir = working_dir / "ptcg_build"
    try:
        if build_dir.exists():
            shutil.rmtree(build_dir, ignore_errors=True)
        build_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy src/ and setup.py to build_dir
        shutil.copytree(src_dir, build_dir / "src")
        shutil.copy2(setup_file, build_dir / "setup.py")
        if (curr_agent_dir / "CMakeLists.txt").exists():
            shutil.copy2(curr_agent_dir / "CMakeLists.txt", build_dir / "CMakeLists.txt")
            
        sys.stderr.write(f"[compile] Copied C++ sources to build dir: {build_dir}\n")
        
        # 5. Run compilation command
        sys.stderr.write("[compile] Compiling C++ ptcg_core extension on-the-fly...\n")
        res = subprocess.run(
            [sys.executable, "setup.py", "build_ext", "--inplace"],
            cwd=str(build_dir),
            capture_output=True,
            text=True
        )
        sys.stderr.write(f"[compile] Compilation stdout:\n{res.stdout}\n")
        sys.stderr.write(f"[compile] Compilation stderr:\n{res.stderr}\n")
        
        if res.returncode != 0:
            sys.stderr.write(f"[compile] Compilation failed with exit code: {res.returncode}\n")
            return False
            
        # 6. Locate compiled .so file
        compiled_so = list(build_dir.glob("ptcg_core*.so"))
        if not compiled_so:
            sys.stderr.write("[compile] Compilation completed but ptcg_core*.so not found.\n")
            return False
            
        # Copy to /kaggle/working
        target_so = working_dir / compiled_so[0].name
        shutil.copy2(compiled_so[0], target_so)
        sys.stderr.write(f"[compile] Successfully copied compiled extension to {target_so}\n")
        
        # Add to sys.path
        if str(working_dir) not in sys.path:
            sys.path.insert(0, str(working_dir))
            
        # Try importing to verify
        import ptcg_core  # type: ignore
        _update_mcts_module(ptcg_core)
        sys.stderr.write("[compile] ptcg_core successfully compiled, loaded, and verified!\n")
        return True
    except Exception as build_err:
        sys.stderr.write(f"[compile] Exception during on-the-fly compilation: {build_err}\n")
        return False

