from loguru import logger


try:
    import PySide6   # noqa: F401
    from .pyside_pandasModel import DataFrameModel   # noqa: F401
except ImportError:
    try:
        import PyQt6  # noqa: F401
        from .pyqt_pandasModel import DataFrameModel  # noqa: F401
    except ImportError as err:
        logger.error('You have to install PyQt6 or PySide6')
        raise err