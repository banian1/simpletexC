import flet as ft
import mathocr
import json
import asyncio
SETTINGS_FILE = "settings.json"


def load_settings():
    try:
        with open(SETTINGS_FILE) as f:
            return json.load(f)
    except:
        return {}


def save_settings(**kwargs):
    data = load_settings()
    data.update(kwargs)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def main(page: ft.Page):
    page.title = "simpletexC"
    settings = load_settings()

    # ---- 主页面控件 ----
    img2ocr = ft.Image(src="src/assets/icon.png", width=400, height=300)
    loading = ft.ProgressRing(width=50, height=50, visible=False)
    img_stack = ft.Stack(
        [
            img2ocr,
            ft.Container(
                content=loading,
                alignment=ft.alignment.Alignment.CENTER,
            ),
        ],
        width=400,
        height=300,
    )
    ocr_result = ft.TextField(
        label="the result of the OCR", expand=1, multiline=True
    )
    render_result = ft.Markdown(value="", expand=True)

    main_view = ft.Column(
        controls=[
            ft.Row([img_stack], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(controls=[ocr_result, render_result]),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )

    # ---- 设置页控件 ----
    uat = ft.TextField(label="UAT", value=settings.get("uat", ""))
    auto_copy = ft.Switch(
        label="识别后自动复制到剪贴板", value=settings.get("auto_copy", True)
    )

    def on_uat_change(e):
        save_settings(uat=uat.value)

    def on_auto_copy_change(e):
        save_settings(auto_copy=auto_copy.value)

    uat.on_change = on_uat_change
    auto_copy.on_change = on_auto_copy_change

    settings_view = ft.Column(
        controls=[
            ft.Text("设置", size=24, weight=ft.FontWeight.BOLD),
            uat,
            auto_copy,
        ],
        expand=True,
    )

    # ---- 页面容器 ----
    content_area = ft.Container(content=main_view, expand=True)

    # ---- 导航栏切换 ----
    def on_nav_change(e):
        if e.control.selected_index == 0:
            content_area.content = main_view
        else:
            content_area.content = settings_view
        page.update()

    nav = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="首页"),
            ft.NavigationBarDestination(icon=ft.Icons.SETTINGS, label="设置"),
        ],
        on_change=on_nav_change,
    )

    # ---- OCR 功能逻辑 ----
    async def paste_img():
        loading.visible = True
        page.update()
        data = await ft.Clipboard().get_image()
        if data:
            img2ocr.src = data
            ocr_result.value = "Processing..."
            page.update()
            with open("temp_image.png", "wb") as f:
                f.write(data)
            ocr_result.value = "$$" + await asyncio.to_thread(mathocr.mathocr, "temp_image.png", uat=uat.value) + "$$"
            render_result.value = ocr_result.value
            page.update()
            ## 自动复制到剪贴板
            if auto_copy.value:
                await ft.Clipboard().set(ocr_result.value)
        else:
            ocr_result.value = "No image data found in clipboard."
            page.update()
        loading.visible = False
        page.update()
        

    async def on_keyboard(e: ft.KeyboardEvent):
        if e.ctrl and e.key == "V":
            await paste_img()

    def on_ocr_change(e):
        render_result.value = ocr_result.value
        page.update()

    ocr_result.on_change = on_ocr_change
    page.on_keyboard_event = on_keyboard

    page.add(
        ft.Column(
            controls=[content_area, nav],
            spacing=0,
            expand=True,
        )
    )


ft.run(main)
