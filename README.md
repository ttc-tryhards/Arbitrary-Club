This is the code for populating the [arbitrary club spreadsheet](https://docs.google.com/spreadsheets/d/1ev4J2turGHjlQH452ngQaGqSRAwMYA47bglJZoPqfsg/edit?gid=0#gid=0).

**Setup**:
Download the files from the repository and place them where you want to store them on your computer. (It's good practice to move something like this out of your downloads folder, for organization.)

**How to use**:
1. Go to the [tetris.com leaderboards](https://docs.google.com/spreadsheets/d/15s4LrzTQpX2lFVsRt_esvPGqveYKgVPmaqks38HzBDw/edit?gid=0#gid=0).
2. Download each of the four tabs of the spreadsheet as a TSV (File -> Download -> Tab Separated Values (.tsv)).
3. Move all of these downloaded files to the folder of the script. You'll want to make sure that the downloaded files names don't have a (1) or a (2) (or any (integer)) after them. This happens when you have another file by the same name in the downloads folder. If repeating this process, make sure to delete the old leaderboards tsvs from your computer. The code won't be able to read the modified names correctly.
4. Run the python script "tiers.py". You'll need some sort of code editor that can run python to do this. I use vscode.
5. After you run the script, double check the console output. If there are any case matching issues in the spreadsheet, it will point them out. If there are issues, you'll need to manually fix them on the leaderboard. If there aren't issues, the code will say so.
6. Open the [arbitrary club spreadsheet](https://docs.google.com/spreadsheets/d/1ev4J2turGHjlQH452ngQaGqSRAwMYA47bglJZoPqfsg/edit?gid=0#gid=0).
7. Navigate to the second tab (Tiers Completion).
8. Make sure you have the top left cell selected.
9. Import the file "output.csv" (File -> Import -> Upload -> Browse -> \*select the file from your computer* -> Import Location = Replace data at selected cell, Detect Automatically -> Import Data)
10. Repeat the same process for tab 3 of the spreadsheet (Tiers Leaderboard), making sure to select the top left cell and this time with the "tiersLeaderboard.csv" file.
