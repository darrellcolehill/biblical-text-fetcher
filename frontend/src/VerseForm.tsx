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

const VerseForm: React.FC = () => {
  const [version, setVersion] = useState('');
  const [book, setBook] = useState('');
  const [chapter, setChapter] = useState('');
  const [verse, setVerse] = useState('');
  const [responseText, setResponseText] = useState('');
  const [copySuccess, setCopySuccess] = useState('');
  const [source, setSource] = useState('GPT');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!book || !chapter || !version) {
      alert('Please fill in both Book, Chapter, and Version');
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

      try {
        setLoading(true);
        const yoinkSource = source === "GPT" ? "GPT" : "BG";
        const response = await fetch(`http://localhost:5000/yoink${yoinkSource}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            "version": version,
            "book": book,
            "chapter": chapter,
            "verses": verseArray,
            "source": source,
          }),
        });

        if (response.ok) {
          const responseData = await response.json();
          setResponseText(responseData.text);
        } else {
          const errorData = await response.json();
          console.error("Error:", errorData);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    }

    console.log(`Book: ${book}, Chapter: ${chapter}, Verse: ${verseArray.length ? verseArray : 'All verses'}, Source: ${source}`);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(responseText).then(() => {
      setCopySuccess('Text copied!');
      setTimeout(() => setCopySuccess(''), 2000);
    }).catch(() => {
      setCopySuccess('Failed to copy text');
    });
  };

  const handleDownload = () => {
    const fileName = `${book}_${chapter}_${verse ? verse.replace(/,/g, '_') : 'All'}_${version}.txt`;
    const blob = new Blob([responseText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url); // Cleanup
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
        <Grid container spacing={2} justifyContent="center">
          <Grid item xs={2}>
            <FormControl fullWidth>
              <InputLabel id="source-label">Source</InputLabel>
              <Select
                labelId="source-label"
                id="source-select"
                value={source}
                label="Source"
                onChange={(e) => setSource(e.target.value)}
              >
                <MenuItem value="GPT">GPT</MenuItem>
                <MenuItem value="Bible Gateway">Bible Gateway</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={2}>
            <TextField
              label="Version"
              value={version}
              onChange={(e) => setVersion(e.target.value)}
              fullWidth
              required
            />
          </Grid>
          <Grid item xs={2}>
            <TextField
              label="Book"
              value={book}
              onChange={(e) => setBook(e.target.value)}
              fullWidth
              required
            />
          </Grid>
          <Grid item xs={2}>
            <TextField
              label="Chapter"
              value={chapter}
              onChange={(e) => setChapter(e.target.value)}
              fullWidth
              required
            />
          </Grid>
          <Grid item xs={2}>
            <TextField
              label="Verse (optional): 1, 2, 3; 1-3"
              value={verse}
              onChange={(e) => setVerse(e.target.value)}
              fullWidth
            />
          </Grid>
        </Grid>
        <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
          Search
        </Button>
      </form>

      {responseText && (
        <Box sx={{ mt: 4, width: '100%', position: 'relative', border: '1px solid #ddd', borderRadius: '8px', padding: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Tooltip title="Copy to Clipboard">
              <IconButton onClick={handleCopy} sx={{ position: 'absolute', top: 8, right: 8 }}>
                <ContentCopyIcon />
              </IconButton>
            </Tooltip>
          </Box>
          <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', mb: 2 }}>
            {responseText}
          </Typography>
          {copySuccess && <Typography variant="body2" color="primary">{copySuccess}</Typography>}
          <Button variant="contained" color="secondary" onClick={handleDownload} sx={{ mt: 2 }}>
            Download as .txt
          </Button>
        </Box>
      )}
    </Box>
  );
};

export default VerseForm;
