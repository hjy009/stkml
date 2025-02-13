from matplotlib.font_manager import FontManager
fm = FontManager()
available_fonts = {f.name for f in fm.ttflist}
print(sorted(available_fonts))