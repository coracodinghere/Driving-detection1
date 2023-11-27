from engine.model import create_model
from engine.dataset import *
from engine.trainer import Trainer
import argparse
import yaml


def Args():
    parser = argparse.ArgumentParser(description="settings")
    parser.add_argument("--images", nargs="+", type=str, required=True)
    parser.add_argument("--device", default='cuda', type=str)
    parser.add_argument("--config", default="configs/coco2017.yml", type=str)

    parser.add_argument("--pretrain_weight", default=None, type=str)
    parser.add_argument("--output_dir", default=None, type=str)
    return parser.parse_args()


def infer():
    args = Args()

    to_size = (288, 512)
    DEVICE = torch.device(args.device)
    config_path = args.config
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # overwrite output_dir and pretrain_weight in config
    if args.pretrain_weight is not None:
        config['pretrain_weight'] = args.pretrain_weight
    if args.output_dir is not None:
        config['output_dir'] = args.output_dir


    val_anno_dir = config['val_anno_dir']

    # create model
    model = create_model(num_classes=config['num_classes']).to(DEVICE)



    # create trainer, begin evaluation
    trainer = Trainer(None, None, model,
                      config['output_dir'], val_anno_dir, base_lr=config['base_lr'],
                      max_epoch=config['max_epoch'],warmup_step=config['warmup_step'],
                      cycle_epoch=config['cycle_epoch'], snapshot_epoch=config['snapshot_epoch'],
                      device=DEVICE, pre_weight_dir=config['pretrain_weight'])

    trainer.predict(args.images, draw_thr=0.5)


if __name__ == '__main__':
    infer()

