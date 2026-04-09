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

QFrame#StepperFrame {
    background: rgba(255, 255, 255, 0.98);
    border: 1px solid #f3d2bc;
    border-radius: 8px;
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

QToolButton#StepperButton {
    background: transparent;
    color: #9a3412;
    border: none;
    border-radius: 6px;
    min-width: 24px;
    max-width: 24px;
    min-height: 24px;
    max-height: 24px;
    font-size: 16px;
    font-weight: 700;
}

QToolButton#StepperButton:hover {
    background: rgba(194, 65, 12, 0.10);
}

QToolButton#StepperButton:pressed {
    background: rgba(194, 65, 12, 0.18);
}

QSpinBox {
    padding: 0;
    min-height: 24px;
    max-height: 24px;
    min-width: 34px;
    max-width: 34px;
    border: none;
    background: transparent;
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
