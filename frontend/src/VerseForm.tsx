import React, { useState } from 'react';
import {
  TextField,
  Button,
  Box,
  Typography,
  Grid,
  IconButton,
  Tooltip,
  MenuItem,
  Select,
  InputLabel,
  FormControl,
  CircularProgress,
} from '@mui/material';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import AddIcon from '@mui/icons-material/Add';
import { saveAs } from 'file-saver';
import JSZip from 'jszip';

const VerseForm: React.FC = () => {
  const [inputRows, setInputRows] = useState([{ version: '', book: '', chapter: '', verse: '', source: 'GPT' }]);
  const [responseTexts, setResponseTexts] = useState<string[]>([]);
  const [copySuccess, setCopySuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAddRow = () => {
    setInputRows([...inputRows, { version: '', book: '', chapter: '', verse: '', source: 'GPT' }]);
  };

  const handleInputChange = (index: number, field: string, value: string) => {
    const newRows = [...inputRows];
    newRows[index][field] = value;
    setInputRows(newRows);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const allResponseTexts: string[] = [];
    const requests = inputRows.map(async (row) => {
      const { version, book, chapter, verse, source } = row;

      if (!book || !chapter || !version) {
        alert('Please fill in both Book, Chapter, and Version for all rows');
        return;
      }

      const versePattern = /^(?:\d+|\d+(?:,\s*\d+)*|\d+-\d+)$/;

      if (verse && !versePattern.test(verse)) {
        alert('Please enter a valid verse format: a single verse (e.g., 1), multiple verses (e.g., 1, 2, 3), or a range (e.g., 1-3)');
        return;
      }

      const verseArray: number[] = [];

      if (verse) {
        const verses = verse.split(',').map(v => v.trim());
        verses.forEach(v => {
          const rangeMatch = v.match(/(\d+)-(\d+)/);
          if (rangeMatch) {
            const start = parseInt(rangeMatch[1]);
            const end = parseInt(rangeMatch[2]);
            verseArray.push(...Array.from({ length: end - start + 1 }, (_, i) => start + i));
          } else {
            verseArray.push(parseInt(v));
          }
        });
      }

      try {
        setLoading(true);
        const yoinkSource = source === "GPT" ? "GPT" : "BG";
        const response = await fetch(`http://localhost:5000/yoink${yoinkSource}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            version,
            book,
            chapter,
            verses: verseArray,
            source,
          }),
        });

        if (response.ok) {
          const responseData = await response.json();
          allResponseTexts.push(responseData.text);
        } else {
          const errorData = await response.json();
          console.error("Error:", errorData);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    });

    await Promise.all(requests);
    setResponseTexts(allResponseTexts);

    if (allResponseTexts.length) {
      const zip = new JSZip();
      allResponseTexts.forEach((text, index) => {
        zip.file(`response_${index + 1}.txt`, text);
      });

      const content = await zip.generateAsync({ type: 'blob' });
      saveAs(content, 'responses.zip');
    }
  };

  const handleCopy = () => {
    const combinedText = responseTexts.join('\n\n');
    navigator.clipboard.writeText(combinedText).then(() => {
      setCopySuccess('Text copied!');
      setTimeout(() => setCopySuccess(''), 2000);
    }).catch(() => {
      setCopySuccess('Failed to copy text');
    });
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: 2,
        maxWidth: 1200,
        margin: '0 auto',
        position: 'relative',
      }}
    >
      {loading && (
        <Box
          sx={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(255, 255, 255, 0.8)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 1000,
          }}
        >
          <CircularProgress />
        </Box>
      )}

      <Typography variant="h4" gutterBottom>
        Verse Lookup
      </Typography>
      <form onSubmit={handleSubmit}>
        {inputRows.map((row, index) => (
          <Grid container spacing={2} justifyContent="center" sx={{ mb: 4 }} key={index}>
            <Grid item xs={2}>
              <FormControl fullWidth>
                <InputLabel id={`source-label-${index}`}>Source</InputLabel>
                <Select
                  labelId={`source-label-${index}`}
                  id={`source-select-${index}`}
                  value={row.source}
                  label="Source"
                  onChange={(e) => handleInputChange(index, 'source', e.target.value)}
                >
                  <MenuItem value="GPT">GPT</MenuItem>
                  <MenuItem value="Bible Gateway">Bible Gateway</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={2}>
              <TextField
                label="Version"
                value={row.version}
                onChange={(e) => handleInputChange(index, 'version', e.target.value)}
                fullWidth
                required
              />
            </Grid>
            <Grid item xs={2}>
              <TextField
                label="Book"
                value={row.book}
                onChange={(e) => handleInputChange(index, 'book', e.target.value)}
                fullWidth
                required
              />
            </Grid>
            <Grid item xs={2}>
              <TextField
                label="Chapter"
                value={row.chapter}
                onChange={(e) => handleInputChange(index, 'chapter', e.target.value)}
                fullWidth
                required
              />
            </Grid>
            <Grid item xs={2}>
              <TextField
                label="Verse (optional): 1, 2, 3; 1-3"
                value={row.verse}
                onChange={(e) => handleInputChange(index, 'verse', e.target.value)}
                fullWidth
              />
            </Grid>
          </Grid>
        ))}
        <IconButton onClick={handleAddRow} sx={{ mb: 2 }}>
          <AddIcon />
        </IconButton>
        <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
          Search
        </Button>
      </form>

      {responseTexts.length > 0 && (
        <Box sx={{ mt: 4, width: '100%', position: 'relative', border: '1px solid #ddd', borderRadius: '8px', padding: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Tooltip title="Copy to Clipboard">
              <IconButton onClick={handleCopy} sx={{ position: 'absolute', top: 8, right: 8 }}>
                <ContentCopyIcon />
              </IconButton>
            </Tooltip>
          </Box>
          <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', mb: 2 }}>
            {responseTexts.join('\n\n')}
          </Typography>
          {copySuccess && <Typography variant="body2" color="primary">{copySuccess}</Typography>}
        </Box>
      )}
    </Box>
  );
};

export default VerseForm;
