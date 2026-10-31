# Physical AI 応用編1 最終課題: でこぼこ地形の速度の指示を4段階に分けて広げる

このリポジトリは Unitree Robotics の [unitree_rl_mjlab](https://github.com/unitreerobotics/unitree_rl_mjlab)(Apache License 2.0)をフォークしたものです。最終課題のために加えた変更は、下の1ファイルだけです。

## 変えたところ

| ファイル | 変更 |
|---|---|
| `src/tasks/velocity/config/go2/__init__.py` | 末尾に課題 `Unitree-Go2-Rough-Gradual` を追加(約25行)。元の課題には手を入れていない |

`Unitree-Go2-Rough` では、学習の5000回目で前進の速度の指示の上限が 1.0 m/s から 2.0 m/s へ一気に広がります。`Unitree-Go2-Rough-Gradual` は、これを4段階に分けて広げます。最後の範囲・地形・報酬は元と同じです。

| 学習の回 | 前進 | 横 |
|---|---|---|
| 0〜 | −0.5〜1.0 m/s | ±0.5 m/s |
| 4000〜 | −0.6〜1.25 | ±0.6 |
| 5500〜 | −0.75〜1.5 | ±0.75 |
| 7000〜 | −0.9〜1.75 | ±0.9 |
| 8500〜 | −1.0〜2.0 | ±1.0 |

## 動かし方

環境は元のREADMEの手順(Ubuntu・NVIDIAのGPU・conda の Python 3.11)で立てます。手元では次の版の調整が必要でした。

```bash
pip install -e .
pip install "mujoco==3.5.0" "warp-lang==1.12.1" scipy
```

学習(4096体・10001回。RTX 5080 1枚で約4時間半):

```bash
python scripts/train.py Unitree-Go2-Rough-Gradual --env.scene.num-envs=4096 --agent.logger=tensorboard
```

比べる相手(元の設定):

```bash
python scripts/train.py Unitree-Go2-Rough --env.scene.num-envs=4096 --agent.logger=tensorboard
```

再生と録画(画面の無い計算機では `MUJOCO_GL=egl`。45秒 = 0.02秒 × 2250コマ):

```bash
MUJOCO_GL=egl python scripts/play.py Unitree-Go2-Rough-Gradual --checkpoint_file=<model_5500.pt> --num_envs=1 --video True --video-length 2250 --video-height 720 --video-width 1280
```

学習済みのモデルのファイルは、このリポジトリには入れていません。

## 結果(TensorBoard の値。左が元の設定、右が4段階に分けた設定)

| 回 | 前進の上限 | 速度のずれ m/s | 地形の段階(0〜9) | 速度に従う点 |
|---|---|---|---|---|
| 4000 | 1.0 → 1.0 | 0.57 → 0.56 | 1.55 → 1.58 | 0.71 → 0.71 |
| 5500 | 2.0 → 1.25 | 1.96 → 0.73 | 0.29 → 2.54 | 0.31 → 0.63 |
| 6000 | 2.0 → 1.5 | 2.05 → 1.18 | 0.30 → 1.49 | 0.34 → 0.52 |
| 8000 | 2.0 → 1.75 | 1.98 → 1.51 | 0.41 → 0.94 | 0.35 → 0.48 |
| 10000 | 2.0 → 2.0 | 2.21 → 1.95 | 0.30 → 0.47 | 0.29 → 0.39 |

上限が1.25 m/sの間は、地形の段階が2.5まで上がりました(元の設定の最高は1.6付近)。1.5 m/s以上に広げると崩れ、最後は元の設定に近い値に戻りました。詳しくは説明資料(PDF)に書いています。

## ライセンス

元のコードと同じ Apache License 2.0 です(`LICENCE`)。上の表の1ファイルを変更しています。
