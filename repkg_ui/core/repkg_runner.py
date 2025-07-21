"""
RePKG UI - Command Runner
========================

Handles execution of RePKG commands with parameter building and logging.
"""

import subprocess
from datetime import datetime
from .file_utils import get_repkg_executable_path
from ..constants import LOG_FILE


class RePKGRunner:
    """Handles execution of RePKG commands with proper parameter building."""
    
    def __init__(self):
        """Initialize the RePKG runner."""
        self.repkg_exe_path = get_repkg_executable_path()
    
    def build_command(self, mode, input_path, output_path="", extract_options=None, info_options=None):
        """
        Build RePKG command with specified parameters.
        
        Args:
            mode (str): Command mode ('extract' or 'info')
            input_path (str): Input file or folder path
            output_path (str): Output directory (for extract mode)
            extract_options (dict): Extract mode options
            info_options (dict): Info mode options
            
        Returns:
            list: Command arguments list
        """
        cmd = [self.repkg_exe_path, mode, input_path]
        
        # Add output path for extract mode
        if output_path and mode == "extract":
            cmd += ["-o", output_path]
        
        # Add extract-specific options
        if mode == "extract" and extract_options:
            cmd.append("-r")  # Recursive is always enabled
            
            if extract_options.get("tex"): cmd.append("-t")
            if extract_options.get("singledir"): cmd.append("-s")
            if extract_options.get("usename"): cmd.append("-n")
            if extract_options.get("no_tex_convert"): cmd.append("--no-tex-convert")
            if extract_options.get("overwrite"): cmd.append("--overwrite")
            if extract_options.get("copyproject"): cmd.append("-c")
            
            if extract_options.get("exts_only"):
                cmd += ["-e", extract_options["exts_only"]]
            if extract_options.get("exts_ignore"):
                cmd += ["-i", extract_options["exts_ignore"]]
        
        # Add info-specific options
        if mode == "info" and info_options:
            if info_options.get("sortby"):
                cmd += ["-b", info_options["sortby"]]
            if info_options.get("sort"): cmd.append("-s")
            if info_options.get("printentries"): cmd.append("-e")
            if info_options.get("info_tex"): cmd.append("-t")
            if info_options.get("projectinfo"):
                cmd += ["-p", info_options["projectinfo"]]
            if info_options.get("title_filter"):
                cmd += ["--title-filter", info_options["title_filter"]]
        
        return cmd
    
    def execute_command(self, cmd, enable_logging=True):
        """
        Execute the RePKG command and return results.
        
        Args:
            cmd (list): Command arguments
            enable_logging (bool): Whether to save to log file
            
        Returns:
            tuple: (output, error, success)
        """
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            output = result.stdout or "[No output]"
            error = result.stderr
            
            # Save to log file if enabled
            if enable_logging:
                self._save_to_log(cmd, output, error)
            
            return output, error, result.returncode == 0
            
        except Exception as e:
            return "", str(e), False
    
    def _save_to_log(self, cmd, output, error):
        """Save command execution details to log file."""
        try:
            log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                # Clean command display for log
                display_cmd = [("repkg" if "_MEI" in c and "RePKG.exe" in c else c) for c in cmd]
                f.write(f"[{log_time}]\n=== Command ===\n" + " ".join(display_cmd) + "\n")
                f.write("=== Output ===\n" + output + "\n")
                if error:
                    f.write("=== Error ===\n" + error + "\n")
                f.write("\n")
        except Exception:
            pass  # Silent fail for logging


# Global runner instance
repkg_runner = RePKGRunner()
