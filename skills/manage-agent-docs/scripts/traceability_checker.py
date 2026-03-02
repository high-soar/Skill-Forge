#!/usr/bin/env python3
"""
traceability_checker.py

MarkdownファイルのYAML Frontmatterを解析し、ドキュメント間の
依存関係（トレーサビリティ）が正しく設定されているかチェックするスクリプト。
"""

import os
import sys
import yaml
import glob
from pathlib import Path
from typing import Dict, Any, List, Optional

def parse_markdown_frontmatter(filepath: str) -> Optional[Dict[str, Any]]:
    """MarkdownファイルからYAML Frontmatterを抽出してパースする"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if content.startswith('---'):
                end_idx = content.find('---', 3)
                if end_idx != -1:
                    frontmatter_text = content[3:end_idx]
                    return yaml.safe_load(frontmatter_text)
    except Exception as e:
        print(f"⚠️ フロントマター解析エラー: {filepath} - {e}")
    return None

def check_traceability(docs_dir: str):
    """指定ディレクトリ内のドキュメントのトレーサビリティを検証する"""
    docs: Dict[str, Dict[str, Any]] = {}
    filepaths = glob.glob(f"{docs_dir}/**/*.md", recursive=True)
    
    if not filepaths:
        print(f"ℹ️ 指定されたディレクトリ '{docs_dir}' にMarkdownファイルが見つかりません。")
        return

    # 1. 全ドキュメントのメタデータを収集
    for filepath in filepaths:
        # README.md やチェックスクリプト対象外のファイルはスキップ
        if os.path.basename(filepath).lower() == 'readme.md':
            continue

        meta = parse_markdown_frontmatter(filepath)
        if meta and 'id' in meta:
            # 重複IDのチェック
            if meta['id'] in docs:
                print(f"❌ エラー: ID '{meta['id']}' が重複しています。({filepath} と {docs[meta['id']]['_filepath']})")
            
            meta['_filepath'] = filepath
            docs[meta['id']] = meta
        elif meta: # FrontmatterはあるがIDがない
             print(f"⚠️ 警告: ファイル '{filepath}' に 'id' が設定されていません。")

    defined_ids = set(docs.keys())
    errors: List[str] = []

    # 2. 参照関係 (implements) の整合性をチェック
    for doc_id, meta in docs.items():
        doc_type = meta.get('type')
        references = meta.get('implements', [])
        
        # implements が文字列の場合はリストに変換
        if isinstance(references, str):
            references = [references]

        if not references and doc_type in ['interface', 'internal_design']:
             errors.append(f"❌ 参照欠落: {doc_type} 型の '{doc_id}' ({meta['_filepath']}) が上位ドキュメントを参照(implements)していません。")

        for ref_id in references:
            if ref_id not in defined_ids:
                errors.append(f"❌ リンク切れ: '{doc_id}' ({meta['_filepath']}) が存在しないID '{ref_id}' を参照しています。")

    # 3. 結果の出力
    if errors:
        print("\n=== トレーサビリティ・エラー ===")
        for err in errors:
            print(err)
        sys.exit(1) # エラーがある場合は終了コード1
    else:
        print("\n✅ 全てのドキュメントのトレーサビリティが正常に確認されました。")
        print(f"検査対象ファイル数: {len(docs)}")
        sys.exit(0)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ドキュメントのトレーサビリティをチェックします。")
    parser.add_argument("docs_dir", type=str, nargs='?', default=".", help="チェック対象のドキュメントディレクトリ (デフォルト: カレントディレクトリ)")
    args = parser.parse_args()

    check_traceability(args.docs_dir)
