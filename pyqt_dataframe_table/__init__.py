__version__ = '0.1.0'

try:
    from PyQt6 import QtCore, QtGui, QtWidgets
    from PyQt6.QtWidgets import QApplication, QTableView
    from PyQt6.QtCore import pyqtSlot as Slot
except ImportError:
    from PySide6 import QtCore, QtGui, QtWidgets  # noqa: F401
    from PySide6.QtWidgets import QApplication, QTableView  # noqa: F401
    from PySide6.QtCore import Slot  # noqa: F401

from .pandasModel import DataFrameModel  # noqa: F401
