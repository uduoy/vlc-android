#!/usr/bin/env python3
"""Apply CJK font patches to the fetched VLC source tree."""

import sys, os

VLC_SRC = 'libvlcjni/vlc'

def patch_platform_fonts():
    path = os.path.join(VLC_SRC, 'modules/text_renderer/freetype/platform_fonts.h')
    with open(path) as f:
        content = f.read()
    content = content.replace(
        '# define SYSTEM_DEFAULT_FONT_FILE           "Roboto-Regular.ttf"',
        '# define SYSTEM_DEFAULT_FONT_FILE           "NotoSansCJK-Regular.ttc"')
    content = content.replace(
        '# define SYSTEM_DEFAULT_MONOSPACE_FONT_FILE "DroidSansMono.ttf"',
        '# define SYSTEM_DEFAULT_MONOSPACE_FONT_FILE "NotoSansCJK-Regular.ttc"')
    with open(path, 'w') as f:
        f.write(content)
    print('Patched platform_fonts.h')

def patch_android_c():
    path = os.path.join(VLC_SRC, 'modules/text_renderer/freetype/fonts/android.c')
    with open(path) as f:
        lines = f.readlines()

    cjk_code = [
        '    {\n',
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
        '                          SYSTEM_FONT_PATH, cjk_font_candidates[i] ) < 0 )\n',
        '                continue;\n',
        '\n',
        '            vlc_family_t *p_family =\n',
        '                NewFamily( fs, cjk_font_candidates[i],\n',
        '                           NULL, &fs->fallback_map, FB_LIST_DEFAULT );\n',
        '            if( p_family )\n',
        '            {\n',
        '                if( !NewFont( psz_fontfile, 0, 0, p_family ) )\n',
        '                    free( psz_fontfile );\n',
        '            }\n',
        '            else\n',
        '                free( psz_fontfile );\n',
        '        }\n',
        '    }\n',
    ]

    for i, line in enumerate(lines):
        if line.rstrip() == '    return VLC_SUCCESS;':
            lines[i:i] = cjk_code
            break

    with open(path, 'w') as f:
        f.writelines(lines)
    print('Patched fonts/android.c')

if __name__ == '__main__':
    patch_platform_fonts()
    patch_android_c()
    print('CJK font patches applied successfully')
