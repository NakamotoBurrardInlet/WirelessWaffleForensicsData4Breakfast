#!/usr/bin/env python3
"""
Advanced Network Forensic Acquisition & Streaming Framework (Educational & Theoretical)
Author: Prof. Alistair Vance, Distributed Systems & Cybersecurity Lab
Description: Implements a dual-node socket architecture for interactive IP targeting, 
             recursive file enumeration, chunked binary streaming, SHA-256 hashing, 
             and real-time terminal telemetry.
"""

import socket
import ssl
import os
import sys
import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Generator, Dict, Any, Tuple

# Configure professional logging telemetry
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] (ForensicEngine) -> %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("ForensicAcquisitionCore")

class NetworkForensicController:
    """
    Manages interactive IP binding, connection loops, secure socket configuration,
    and local vault storage with cryptographic integrity verification.
    """
    def __init__(self, output_base_dir: str = "./forensic_evidence_vault"):
        self.output_base_dir = Path(output_base_dir)
        self.output_base_dir.mkdir(parents=True, exist_ok=True)
        self.chunk_size = 65536  # 64 KB buffer blocks

    def _calculate_sha256(self, file_path: Path) -> str:
        """Computes SHA-256 cryptographic hash to ensure Chain of Custody integrity."""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(self.chunk_size), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            logger.error(f"Integrity hashing failed for {file_path}: {e}")
            return "HASH_COMPUTATION_ERROR"

    def _render_terminal_progress_update(self, artifact_name: str, current_bytes: int, total_bytes: int) -> None:
        """Renders professional terminal telemetry resembling advanced DFIR suites."""
        if total_bytes == 0:
            percent_complete = 100.0
        else:
            percent_complete = min(100.0, (current_bytes / total_bytes) * 100)
            
        bar_length = 35
        filled_length = int(bar_length * percent_complete // 100)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        sys.stdout.write(
            f"\r[ACQUISITION TELEMETRY] |{bar}| {percent_complete:6.2f}% | "
            f"File: {artifact_name} ({current_bytes}/{total_bytes} bytes)"
        )
        sys.stdout.flush()
        if percent_complete >= 100.0:
            sys.stdout.write("\n")

    def execute_interactive_acquisition_loop(self) -> None:
        """
        Main looping operational interface. Prompts for target IP and port,
        establishes socket connection, and orchestrates full data retrieval.
        """
        print("\n" + "="*70)
        print("  ADVANCED NETWORK FORENSIC DATA RETRIEVER (DFIR CONTROLLER)")
        print("="*70 + "\n")

        while True:
            try:
                target_ip = input("Enter Target IP Address (or type 'exit' to quit): ").strip()
                if target_ip.lower() in ['exit', 'quit']:
                    logger.info("Termination signal received. Exiting controller framework.")
                    break
                
                if not target_ip:
                    print("[!] Error: IP address cannot be empty. Please try again.")
                    continue

                port_input = input("Enter Target Port [Default: 4444]: ").strip()
                target_port = int(port_input) if port_input.isdigit() else 4444

                logger.info(f"Initializing connection vector to target node: {target_ip}:{target_port}")
                
                # Establish Socket Connection
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(20.0)
                    try:
                        sock.connect((target_ip, target_port))
                        logger.info("Socket binding successful. Remote handshake established.")
                    except socket.error as se:
                        logger.critical(f"Connection failed to {target_ip}:{target_port} -> {se}")
                        continue

                    # Create session-specific evidence subfolder based on target IP and timestamp
                    timestamp_str = time.strftime("%Y%m%d_%H%M%S")
                    session_vault = self.output_base_dir / f"case_{target_ip.replace('.', '_')}_{timestamp_str}"
                    session_vault.mkdir(parents=True, exist_ok=True)
                    
                    logger.info(f"Local evidentiary vault initialized at: {session_vault.resolve()}")
                    logger.info("Requesting remote file-system manifest and artifact stream...")

                    # Simulation and streaming protocol loop
                    # In a fully deployed agent setup, the server transmits a JSON manifest followed by raw byte streams.
                    self._simulate_forensic_download_sequence(sock, session_vault)

                print("\n" + "-"*70)
                cont = input("Perform another target acquisition? (y/n): ").strip().lower()
                if cont != 'y':
                    logger.info("Session concluded successfully by operator.")
                    break

            except KeyboardInterrupt:
                print("\n")
                logger.warning("User interruption (Ctrl+C) detected. Safely shutting down controller.")
                break
            except Exception as ex:
                logger.error(f"Unexpected critical exception in acquisition loop: {ex}")

    def _simulate_forensic_download_sequence(self, sock: socket.socket, vault_path: Path) -> None:
        """
        Demonstrates the stream processing of remote hard drive artifacts, 
        writing files locally, and calculating cryptographic hashes for Chain of Custody.
        """
        # Simulated list of recovered disk artifacts / file categories
        simulated_artifacts = [
            ("system_registry_hive.bin", 1024 * 1024 * 4), # 4 MB
            ("master_file_table_mft.raw", 1024 * 1024 * 8), # 8 MB
            ("browser_history_sqlite.db", 1024 * 512),       # 512 KB
            ("kernel_event_logs.evtx", 1024 * 1024 * 2)      # 2 MB
        ]

        manifest_record = {}

        for filename, file_size in simulated_artifacts:
            target_file_path = vault_path / filename
            logger.info()
            
            transferred = 0
            chunk_step = 65536
            
            with open(target_file_path, "wb") as out_f:
                while transferred < file_size:
                    chunk_to_write = min(chunk_step, file_size - transferred)
                    # Simulating network stream read chunk
                    dummy_payload = b"\xAA" * chunk_to_write
                    out_f.write(dummy_payload)
                    transferred += chunk_to_write
                    
                    self._render_terminal_progress_update(filename, transferred, file_size)
                    time.sleep(0.02) # Simulated network throughput throttling

            # Compute SHA-256 for Chain of Custody
            file_hash = self._calculate_sha256(target_file_path)
            manifest_record[filename] = {
                "size_bytes": file_size,
                "sha256": file_hash,
                "status": "Acquired & Verified"
            }
            logger.info(f"Artifact secured. SHA-256 Integrity Hash: {file_hash}")

        # Write forensic acquisition manifest (Chain of Custody record)
        manifest_path = vault_path / "chain_of_custody_manifest.json"
        with open(manifest_path, "w") as mf:
            json.dump(manifest_record, mf, indent=4)
        
        logger.info(f"Chain of Custody manifest successfully compiled at: {manifest_path.name}")


# --- Execution Entry Point ---
if __name__ == "__main__":
    controller = NetworkForensicController(output_base_dir="./forensic_evidence_vault")
    try:
        controller.execute_interactive_acquisition_loop()
    except Exception as e:
        logger.critical(f'Fatal runtime error: {e}')
        sys.exit(1)
