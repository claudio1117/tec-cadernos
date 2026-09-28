from __future__ import annotations

import argparse
from pathlib import Path

from .processing import ProcessingError, process_materials


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("o valor deve ser maior que zero")
    return number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python3 -m estrategia",
        description="Prepara os PDFs baixados para consumo por arquivos estruturados.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    process = subparsers.add_parser(
        "processar-materiais",
        help="valida PDFs, extrai textos e gera manifesto, índice e relatório",
    )
    process.add_argument(
        "--manifesto-fonte",
        type=Path,
        help="manifesto bruto do downloader (detectado automaticamente quando há apenas um)",
    )
    process.add_argument(
        "--saida",
        type=Path,
        default=PROJECT_ROOT / "data" / "processados",
        help="diretório-base dos JSONs processados",
    )
    process.add_argument(
        "--textos",
        type=Path,
        default=PROJECT_ROOT / "textos",
        help="diretório-base dos textos extraídos",
    )
    process.add_argument(
        "--limite",
        type=_positive_int,
        help="processa no máximo esta quantidade de PDFs pendentes (piloto)",
    )
    process.add_argument(
        "--forcar",
        action="store_true",
        help="refaz a extração mesmo quando PDF e texto não mudaram",
    )
    process.add_argument(
        "--timeout",
        type=_positive_int,
        default=300,
        help="limite em segundos para cada PDF (padrão: 300)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "processar-materiais":
        try:
            result = process_materials(
                project_root=PROJECT_ROOT,
                source_manifest=args.manifesto_fonte,
                output_root=args.saida,
                texts_root=args.textos,
                limit=args.limite,
                force=args.forcar,
                timeout=args.timeout,
            )
        except ProcessingError as exc:
            parser.error(str(exc))

        summary = result.summary
        print("Processamento concluído")
        print(f"  PDFs no manifesto: {summary['total_materiais']}")
        print(f"  processados: {summary['processados']}")
        print(f"  ignorados (sem mudança): {summary['ignorados']}")
        print(f"  pendentes: {summary['pendentes']}")
        print(f"  erros: {summary['erros']}")
        print(f"  manifesto: {result.manifest_path}")
        print(f"  índice: {result.index_path}")
        print(f"  relatório: {result.report_path}")
        return 1 if summary["erros"] else 0

    parser.error(f"comando desconhecido: {args.command}")
    return 2
