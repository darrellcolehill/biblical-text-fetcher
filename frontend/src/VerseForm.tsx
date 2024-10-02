import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Grid, IconButton, Tooltip, MenuItem, Select, InputLabel, FormControl } from '@mui/material';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';

const VerseForm: React.FC = () => {
  const [version, setVersion] = useState('');
  const [book, setBook] = useState('');
  const [chapter, setChapter] = useState('');
  const [verse, setVerse] = useState('');
  const [responseText, setResponseText] = useState(''); // State to hold the response text
  const [copySuccess, setCopySuccess] = useState(''); // State to handle copy success message
  const [source, setSource] = useState('GPT'); // State to handle the source selection

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Check if Book, Chapter, and Version are filled
    if (!book || !chapter || !version) {
      alert('Please fill in both Book, Chapter, and Version');
      return;
    }

    // Regular expression to validate verse input
    const versePattern = /^(?:\d+|\d+(?:,\s*\d+)*|\d+-\d+)$/;

    // Check if the verse input matches the required formats
    if (verse && !versePattern.test(verse)) {
      alert('Please enter a valid verse format: a single verse (e.g., 1), multiple verses (e.g., 1, 2, 3), or a range (e.g., 1-3)');
      return;
    }

    const verseArray: number[] = [];

    if (verse) {
      const verses = verse.split(',').map(v => v.trim());

      verses.forEach(v => {
        const rangeMatch = v.match(/(\d+)-(\d+)/); // Check for range

        if (rangeMatch) {
          const start = parseInt(rangeMatch[1]);
          const end = parseInt(rangeMatch[2]);
          verseArray.push(...Array.from({ length: end - start + 1 }, (_, i) => start + i));
        } else {
          verseArray.push(parseInt(v));
        }
      });

      try {
        const yoinkSource = source == "GPT" ? "GPT" : "BG"
        const text = await fetch(`http://localhost:5000/yoink${yoinkSource}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            "version": version,
            "book": book,
            "chapter": chapter,
            "verses": verseArray,
            "source": source // Include source in the request
          })
        });

        if (text.ok) {
          const responseData = await text.json(); // Parse the JSON response
          setResponseText(responseData.text); // Store the response text
        } else {
          // Handle error response
          const errorData = await text.json();
          console.error("Error:", errorData);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }

    console.log(`Book: ${book}, Chapter: ${chapter}, Verse: ${verseArray.length ? verseArray : 'All verses'}, Source: ${source}`);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(responseText).then(() => {
      setCopySuccess('Text copied!');
      setTimeout(() => setCopySuccess(''), 2000); // Clear success message after 2 seconds
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
      }}
    >
      <Typography variant="h4" gutterBottom>
        Verse Lookup
      </Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={2} justifyContent="center"> {/* Center align the grid items */}
          {/* Dropdown for selecting source (GPT or Bible Gateway) */}
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

          {/* Other form inputs */}
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
        </Box>
      )}
    </Box>
  );
};

export default VerseForm;
