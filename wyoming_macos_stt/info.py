from wyoming.info import AsrModel, AsrProgram, Attribution, Info

from . import __version__


def get_wyoming_info(name):
    return Info(
        asr=[
            AsrProgram(
                name=name,
                description="Speech-to-Text on macOS using yap CLI tool",
                attribution=Attribution(
                    name="Finn Voorhees",
                    url="https://github.com/finnvoor/yap",
                ),
                installed=True,
                version=__version__,
                models=[
                    AsrModel(
                        name="macos-stt",
                        description="Speech-to-Text on macOS using yap CLI tool",
                        attribution=Attribution(
                            name="Apple",
                            url="https://developer.apple.com/documentation/speech",
                        ),
                        installed=True,
                        languages=[
                            "fr_CA",
                            "fr_CH",
                            "fr_FR",
                            "fr_BE",
                            "ko_KR",
                            "pt_BR",
                            "de_AT",
                            "de_CH",
                            "de_DE",
                            "it_CH",
                            "it_IT",
                            "zh_CN",
                            "zh_TW",
                            "es_CL",
                            "es_MX",
                            "es_ES",
                            "es_US",
                            "en_CA",
                            "en_SG",
                            "en_GB",
                            "en_ZA",
                            "en_AU",
                            "en_US",
                            "en_IE",
                            "en_NZ",
                            "en_IN",
                            "yue_CN",
                            "zh_HK",
                            "ar_SA",
                            "ja_JP",
                        ],
                        version="1",
                    )
                ],
            )
        ],
    )
