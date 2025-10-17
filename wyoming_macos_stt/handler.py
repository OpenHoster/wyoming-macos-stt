"""Event handler for clients of the server."""

import argparse
import asyncio
import logging
import os
import tempfile
import time
import wave
from typing import Optional

from wyoming.asr import Transcribe, Transcript
from wyoming.audio import AudioChunk, AudioStop
from wyoming.event import Event
from wyoming.info import Describe
from wyoming.server import AsyncEventHandler

from .info import get_wyoming_info

_LOGGER = logging.getLogger("wyoming-macos-stt")


class MacosSTTEventHandler(AsyncEventHandler):
    """Event handler for clients."""

    def __init__(
        self,
        cli_args: argparse.Namespace,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.cli_args = cli_args
        self.wyoming_info_event = get_wyoming_info(self.cli_args.service_name).event()
        self._wav_dir = tempfile.TemporaryDirectory()
        self._wav_path = os.path.join(self._wav_dir.name, "speech.wav")
        self._wav_file: Optional[wave.Wave_write] = None
        self._language = None

    async def handle_event(self, event: Event) -> bool:
        if AudioChunk.is_type(event.type):
            chunk = AudioChunk.from_event(event)

            if self._wav_file is None:
                self._wav_file = wave.open(self._wav_path, "wb")
                self._wav_file.setframerate(chunk.rate)
                self._wav_file.setsampwidth(chunk.width)
                self._wav_file.setnchannels(chunk.channels)

            self._wav_file.writeframes(chunk.audio)
            return True

        if AudioStop.is_type(event.type):
            assert self._wav_file is not None

            self._wav_file.close()
            self._wav_file = None

            command = f"yap {self.cli_args.yap_args}"
            command += f" -l {self._language} " if self._language else " "
            command += self._wav_path
            _LOGGER.debug(f"Runnning command: {command}")
            start_time = time.time()
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            end_time = time.time()
            _LOGGER.debug(
                f"Command execution duration: {end_time - start_time} seconds"
            )
            if proc.returncode == 0:
                text = stdout.decode()
                _LOGGER.debug(f"Transcribed text: {text}")
                await self.write_event(Transcript(text=text).event())
            else:
                _LOGGER.error(f"Command failed with return code {proc.returncode}")
                _LOGGER.error(stderr.decode())

            return False

        if Transcribe.is_type(event.type):
            transcribe = Transcribe.from_event(event)
            if transcribe.language:
                self._language = transcribe.language
                _LOGGER.debug("Language set to %s", transcribe.language)
            return True

        if Describe.is_type(event.type):
            await self.write_event(self.wyoming_info_event)
            _LOGGER.debug("Sent info")
            return True

        return True
