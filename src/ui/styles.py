APP_STYLESHEET = """
QWidget {
    background: transparent;
    color: #1d2939;
    font-family: "PingFang SC", "Microsoft YaHei", "Segoe UI";
}

QFrame#Card {
    background: rgba(255, 250, 245, 0.97);
    border-radius: 28px;
    border: 1px solid rgba(163, 98, 62, 0.10);
}

QFrame#SettingsPanel {
    background: rgba(255, 255, 255, 0.62);
    border-radius: 22px;
    border: 1px solid rgba(194, 65, 12, 0.08);
}

QFrame#SettingRow {
    background: transparent;
}

QFrame#TitleBar {
    background: transparent;
}

QLabel#TitleLabel {
    font-size: 17px;
    font-weight: 700;
    color: #7c2d12;
    min-height: 24px;
}

QPushButton#TitleButton {
    background: rgba(124, 45, 18, 0.08);
    color: #7c2d12;
    border: none;
    border-radius: 12px;
    padding: 8px 14px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#TitleButton:hover {
    background: rgba(124, 45, 18, 0.14);
}

QPushButton#TitleButton:pressed {
    background: rgba(124, 45, 18, 0.20);
}

QPushButton {
    background: #c2410c;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 14px;
    font-weight: 700;
}

QPushButton:hover {
    background: #9a3412;
}

QPushButton:pressed {
    background: #7c2d12;
}

QPushButton[variant="secondary"] {
    background: #ffedd5;
    color: #7c2d12;
}

QPushButton[variant="secondary"]:hover {
    background: #fed7aa;
}

QPushButton[variant="secondary"]:pressed {
    background: #fdba74;
}

QToolButton#SpinButton {
    background: rgba(194, 65, 12, 0.08);
    color: #9a3412;
    border: none;
    border-radius: 7px;
    min-width: 26px;
    max-width: 26px;
    min-height: 26px;
    max-height: 26px;
    font-size: 16px;
    font-weight: 700;
}

QToolButton#SpinButton:hover {
    background: rgba(194, 65, 12, 0.16);
}

QToolButton#SpinButton:pressed {
    background: rgba(194, 65, 12, 0.24);
}

QSpinBox {
    padding: 0 6px;
    min-height: 32px;
    max-height: 32px;
    min-width: 58px;
    max-width: 58px;
    border-radius: 8px;
    border: 1px solid #fed7aa;
    background: rgba(255, 255, 255, 0.96);
    font-size: 14px;
    font-weight: 600;
    color: #7c2d12;
    qproperty-alignment: AlignCenter;
}

QSpinBox::up-button, QSpinBox::down-button {
    width: 0px;
    border: none;
    background: transparent;
}

QSpinBox::up-arrow, QSpinBox::down-arrow {
    width: 0px;
    height: 0px;
}

QCheckBox {
    spacing: 12px;
    font-size: 13px;
    font-weight: 600;
    color: #7c2d12;
}

QCheckBox::indicator {
    width: 42px;
    height: 24px;
}

QCheckBox::indicator:unchecked {
    border: none;
    border-radius: 12px;
    background: #e7d7ca;
}

QCheckBox::indicator:checked {
    border: none;
    border-radius: 12px;
    background: #fb923c;
}

QLabel#SettingLabel {
    font-size: 14px;
    font-weight: 600;
    color: #7c2d12;
    min-height: 24px;
}

QLabel#MinuteLabel {
    font-size: 13px;
    color: #b45309;
    min-height: 24px;
}

QLabel#FooterLabel {
    font-size: 12px;
    color: rgba(124, 45, 18, 0.45);
}
"""
