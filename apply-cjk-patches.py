#!/usr/bin/env python3
"""Apply CJK font patches to VLC 3.0 source tree."""

import sys, os, re

VLC_SRC = 'libvlcjni/vlc'

def patch_platform_fonts():
    path = os.path.join(VLC_SRC, 'modules/text_renderer/freetype/platform_fonts.h')
    with open(path) as f:
        content = f.read()

    # VLC 3.0: full paths in macros
    content = content.replace(
        '# define SYSTEM_DEFAULT_FONT_FILE "/system/fonts/Roboto-Regular.ttf"',
        '# define SYSTEM_DEFAULT_FONT_FILE "/system/fonts/NotoSansCJK-Regular.ttc"')
    content = content.replace(
        '# define SYSTEM_DEFAULT_MONOSPACE_FONT_FILE "/system/fonts/DroidSansMono.ttf"',
        '# define SYSTEM_DEFAULT_MONOSPACE_FONT_FILE "/system/fonts/NotoSansCJK-Regular.ttc"')

    with open(path, 'w') as f:
        f.write(content)
    print('[OK] platform_fonts.h')

def patch_android_c():
    path = os.path.join(VLC_SRC, 'modules/text_renderer/freetype/fonts/android.c')
    with open(path) as f:
        lines = f.readlines()

    cjk_code = [
        '\n',
        '    /* hardcoded CJK font fallbacks for Chinese subtitle support */\n',
        '    {\n',
        '        filter_sys_t *p_sys = p_filter->p_sys;\n',
        '        static const char *const cjk_font_candidates[] = {\n',
        '            "NotoSansCJK-Regular.ttc",\n',
        '            "NotoSansSC-Regular.otf",\n',
        '            "NotoSansTC-Regular.otf",\n',
        '            "MiSans-Regular.ttf",\n',
        '            "HarmonyOS_Sans_SC_Regular.ttf",\n',
        '            "OPPOSans-Regular.ttf",\n',
        '            NULL\n',
        '        };\n',
        '\n',
        '        for( int i = 0; cjk_font_candidates[i] != NULL; i++ )\n',
        '        {\n',
        '            char *psz_fontfile;\n',
        '            if( asprintf( &psz_fontfile, "%s/%s",\n',
        '                          ANDROID_FONT_PATH, cjk_font_candidates[i] ) < 0 )\n',
        '                continue;\n',
        '\n',
        '            vlc_family_t *p_family =\n',
        '                NewFamily( p_filter, cjk_font_candidates[i],\n',
        '                           NULL, &p_sys->fallback_map, FB_LIST_DEFAULT );\n',
        '            if( p_family )\n',
        '            {\n',
        '                if( !NewFont( psz_fontfile, 0, false, false, p_family ) )\n',
        '                    free( psz_fontfile );\n',
        '            }\n',
        '            else\n',
        '                free( psz_fontfile );\n',
        '        }\n',
        '    }\n',
    ]

    # insert CJK code at the LAST return VLC_SUCCESS (inside Android_Prepare)
    last_idx = None
    for i, line in enumerate(lines):
        if line.rstrip() == '    return VLC_SUCCESS;':
            last_idx = i

    if last_idx is not None:
        lines[last_idx:last_idx] = cjk_code
    else:
        print('[ERROR] could not find insertion point in fonts/android.c')

    with open(path, 'w') as f:
        f.writelines(lines)
    print('[OK] fonts/android.c')

if __name__ == '__main__':
    patch_platform_fonts()
    patch_android_c()
    print('CJK font patches applied successfully (VLC 3.0)')
