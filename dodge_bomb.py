import os
import random
import sys
import time
import pygame as pg

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0)
}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRectまたは爆弾Rect
    戻り値：判定結果タプル（横方向,縦方向）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  #横はみだしチェック
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  #縦はみだしチェック
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    引数:screen Surface
    戻り値:なし
    """
    blackout = pg.Surface((WIDTH, HEIGHT))  # ブラックアウト用のSurface
    blackout.fill((0, 0, 0))
    blackout.set_alpha(128)  # 半透明
    
    # Game Over
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rct = text.get_rect()
    text_rct.center = WIDTH // 2, HEIGHT // 2
    
    cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.3)
    cry_rct_left = cry_img.get_rect()  #泣いているこうかとん左
    cry_rct_right = cry_img.get_rect()  #泣いているこうかとん右
    cry_rct_left.center = text_rct.left -50, HEIGHT // 2  #　場所調整
    cry_rct_right.center = text_rct.right +50, HEIGHT // 2  #　場所調整
    
    # 画面に表示
    screen.blit(blackout, (0, 0))
    screen.blit(cry_img, cry_rct_left)
    screen.blit(text, text_rct)
    screen.blit(cry_img, cry_rct_right)
    pg.display.update()
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))  #空のSurface
    pg.draw.circle(bb_img, (255,0,0), (10,10), 10)  #円描写
    bb_img.set_colorkey((0,0,0))  #背景透明
    bb_rct = bb_img.get_rect()  #爆弾rct
    bb_rct.centerx = random.randint(0, WIDTH)  # 爆弾横座標
    bb_rct.centery = random.randint(0, HEIGHT)  # 爆弾縦座標
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  #こうかとんと爆弾が重なったら
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 横方向の移動量
                sum_mv[1] += mv[1]  # 縦方向の移動量


        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  #画面外なら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  #移動をなかったことにする
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向に出ていたら
            vx *= -1
        if not tate:  # 縦方向に出ていたら
            vy *= -1
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
