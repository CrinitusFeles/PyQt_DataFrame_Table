import pandas as pd
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QTableView
from loguru import logger

def calculate_color(val, row: int, column: str,
                    mask, ok_color, err_color):
    if column == 'ErrCnt':
        if val > 0:
            return QtGui.QBrush(err_color)
    if mask[row]:
        return QtGui.QBrush(ok_color)  # QtCore.Qt.GlobalColor.white
    else:
        return QtGui.QBrush(err_color)

class DataFrameModel(QtCore.QAbstractTableModel):
    DtypeRole: int = QtCore.Qt.ItemDataRole.UserRole + 1000
    ValueRole: int = QtCore.Qt.ItemDataRole.UserRole + 1001

    def __init__(self, df=pd.DataFrame(), mask: pd.Series=pd.Series()) -> None:
        super().__init__()
        self._df: pd.DataFrame = df
        self.values_mask: pd.Series[bool] = mask
        self.palette = 'light'

    def setDataFrame(self, dataframe: pd.DataFrame, mask: pd.Series) -> None:
        self.beginResetModel()
        self._df = dataframe.copy()
        self.values_mask = mask.copy()
        self.endResetModel()

    @QtCore.pyqtSlot(int, QtCore.Qt.Orientation)
    def headerData(self, section: int, orientation: QtCore.Qt.Orientation,
                   role: int = QtCore.Qt.ItemDataRole.DisplayRole):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                return self._df.columns[section]
            else:
                header: str = ''
                try:
                    header = str(self._df.index[section])
                except IndexError as err:
                    logger.error(f'{err}\n{self._df}\n{section=}')
                return header
        return QtCore.QVariant()

    def rowCount(self, parent=QtCore.QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return self._df.columns.size

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount() and 0 <= index.column() < self.columnCount()):
            return QtCore.QVariant()
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        dt = self._df[col].dtype

        val = self._df.iloc[row][col]
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if isinstance(val, float):
                return str(f'{val:.2f}')
            else:
                return str(val)
        elif role == QtCore.Qt.ItemDataRole.BackgroundRole:
            r = index.row()
            if self.palette == 'dark':
                ok_color = QtCore.Qt.GlobalColor.black
                err_color = QtCore.Qt.GlobalColor.darkRed
            else:
                ok_color = QtCore.Qt.GlobalColor.white
                err_color = QtGui.QColor("#DD571C")
            color: QtGui.QBrush = calculate_color(val, r, col, self.values_mask,
                                                  ok_color, err_color)
            return color
        elif role == DataFrameModel.ValueRole:
            return val
        if role == DataFrameModel.DtypeRole:
            return dt
        return QtCore.QVariant()

    def roleNames(self):
        roles = {
            QtCore.Qt.ItemDataRole.DisplayRole: b'display',
            DataFrameModel.DtypeRole: b'dtype',
            DataFrameModel.ValueRole: b'value'
        }
        return roles


if __name__ == '__main__':

    df_raw = pd.DataFrame({'a': ['Mary', 'Jim', 'John'],
                    'b': [100, 200, 300],
                    'IsErr': [True, False, True],
                    'c': ['a', 'b', 'c']})
    df = df_raw.drop('IsErr', axis=1)
    mask = df_raw['IsErr']
    model = DataFrameModel(df, mask)
    app = QApplication([])
    view = QTableView()
    view.setModel(model)
    view.resize(800, 600)
    view.show()
    app.exec()