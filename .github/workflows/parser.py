import os
from glob import iglob
from multiprocessing.pool import ThreadPool
from functools import partial


class FileManager:
    """Class to manage file and folders."""

    def __init__(self, artifacts_path: str) -> None:
        self.artifacts_path = artifacts_path
        self.create_folder(artifacts_path)

    def create_folder(self, path: str) -> None:
        """Create folders (only if they don't exist)."""
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        except OSError as error:
            print(error)

    def create_files_from_list(self, list: list[str], path: str) -> None:
        """Create files from a list of strings under a specific path."""
        file_name = path.split('.md')[0]
        self.create_folder(f'{self.artifacts_path}/{file_name}')
        for d in list:
            with open(f'{self.artifacts_path}/{file_name}/{d["name"]}.yaml',
                      mode='w') as file:
                file.write(d['content'])


class MarkdownParser:
    """Class to parse markdown files."""

    def __init__(self, manifests_path: str) -> None:
        self.manifests_path = manifests_path
        self.file_manager = FileManager(manifests_path)

    def parse(self) -> None:
        files: list[str] = [
            x for x in iglob(os.path.join('./*/*/*.md'), recursive=True)
            if not x.endswith('README.md')
        ]
        with ThreadPool() as pool:
            pool.map(partial(self.parse_and_save), files)

    def parse_and_save(self, path: str) -> None:
        files = self.parse_file(path)
        self.file_manager.create_files_from_list(files, path)

    def parse_file(self, path: str) -> list[dict[str, str]]:
        """Parse a markdown file to extract code snippets."""
        files: list[dict[str, str]] = []
        with open(path, mode='r') as file:
            code_snippets: int = 0
            is_code_block: bool = False
            is_metadata_block: bool = False
            for line in file:
                if line.startswith('```'):
                    is_code_block = not is_code_block
                    if is_code_block:
                        files.append({'name': '', 'content': ''})
                        code_snippets += 1
                if is_metadata_block:
                    files[code_snippets -
                          1]['name'] = line.split('name:')[1].strip()
                    is_metadata_block = False
                if is_code_block and not line.startswith('```'):
                    if line.startswith('metadata'):
                        is_metadata_block = True
                    files[code_snippets - 1]['content'] += line
        return files


def main():
    """Verify Markdown code snippets."""
    markdown_parser: MarkdownParser = MarkdownParser('manifests')
    markdown_parser.parse()


if __name__ == '__main__':
    main()
