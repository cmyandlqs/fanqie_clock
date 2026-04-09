APP_STYLESHEET = """
QWidget {
    background: transparent;
    color: #1d2939;
    font-family: "PingFang SC", "Microsoft YaHei", "Segoe UI";
}

QFrame#Card {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(255, 252, 248, 0.98),
        stop:0.45 rgba(255, 248, 241, 0.96),
        stop:1 rgba(255, 244, 235, 0.97));
    border-radius: 28px;
    border: 1px solid rgba(163, 98, 62, 0.12);
}

QFrame#SettingsPanel {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(255, 255, 255, 0.78),
        stop:1 rgba(255, 248, 242, 0.70));
    border-radius: 22px;
    border: 1px solid rgba(194, 65, 12, 0.08);
}

QFrame#SettingRow {
    background: transparent;
}

QFrame#StepperFrame {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(255, 255, 255, 0.98),
        stop:1 rgba(255, 249, 244, 0.96));
    border: 1px solid #f1cfb8;
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
    letter-spacing: 0.3px;
}

QPushButton#TitleButton {
    background: rgba(255, 255, 255, 0.62);
    color: #7c2d12;
    border: 1px solid rgba(124, 45, 18, 0.08);
    border-radius: 13px;
    padding: 8px 14px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#TitleButton:hover {
    background: rgba(255, 255, 255, 0.78);
}

QPushButton#TitleButton:pressed {
    background: rgba(248, 236, 225, 0.92);
}

QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #fb923c,
        stop:1 #c2410c);
    color: white;
    border: 1px solid rgba(154, 52, 18, 0.18);
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 14px;
    font-weight: 700;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #fdba74,
        stop:1 #ea580c);
}

QPushButton:pressed {
    background: #b45309;
}

QPushButton[variant="secondary"] {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(255, 255, 255, 0.92),
        stop:1 rgba(255, 237, 213, 0.95));
    color: #7c2d12;
    border: 1px solid rgba(194, 65, 12, 0.10);
}

QPushButton[variant="secondary"]:hover {
    background: rgba(255, 243, 229, 0.98);
}

QPushButton[variant="secondary"]:pressed {
    background: rgba(255, 228, 201, 0.98);
}

QToolButton#StepperButton {
    background: transparent;
    color: #9a3412;
    border: none;
    border-radius: 6px;
    min-width: 24px;
    max-width: 24px;
    min-height: 22px;
    max-height: 22px;
    padding: 0;
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
    min-height: 22px;
    max-height: 22px;
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
    font-weight: 500;
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
