from i18n import t


def test_translation_supported_language() -> None:
    assert t("ru", "ask_first_name") == "Введите ваше имя:"


def test_translation_fallback_to_uz_when_language_missing() -> None:
    assert t("de", "ask_first_name") == "Ismingizni kiriting:"


def test_translation_missing_key_returns_key() -> None:
    assert t("uz", "nonexistent_key") == "nonexistent_key"
