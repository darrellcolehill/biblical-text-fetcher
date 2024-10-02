import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Grid } from '@mui/material';

const VerseForm: React.FC = () => {
  const [version, setVersion] = useState('');
  const [book, setBook] = useState('');
  const [chapter, setChapter] = useState('');
  const [verse, setVerse] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
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

    // Parse the verse input
    const verseArray: number[] = [];

    if (verse) {
      const verses = verse.split(',').map(v => v.trim()); // Split by comma

      verses.forEach(v => {
        const rangeMatch = v.match(/(\d+)-(\d+)/); // Check for range

        if (rangeMatch) {
          // If it's a range, generate all numbers from start to end
          const start = parseInt(rangeMatch[1]);
          const end = parseInt(rangeMatch[2]);
          verseArray.push(...Array.from({ length: end - start + 1 }, (_, i) => start + i));
        } else {
          // Otherwise, just add the single number
          verseArray.push(parseInt(v));
        }
      });

      console.log(verses)
    }

    // Proceed with form submission logic
    console.log(`Book: ${book}, Chapter: ${chapter}, Verse: ${verseArray.length ? verseArray : 'All verses'}`);
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
        <Grid container spacing={2}>
          <Grid item xs={3}>
            <TextField
              label="Version"
              value={version}
              onChange={(e) => setVersion(e.target.value)}
              fullWidth
              required
            />
          </Grid>
          <Grid item xs={3}>
            <TextField
              label="Book"
              value={book}
              onChange={(e) => setBook(e.target.value)}
              fullWidth
              required
            />
          </Grid>
          <Grid item xs={3}>
            <TextField
              label="Chapter"
              value={chapter}
              onChange={(e) => setChapter(e.target.value)}
              fullWidth
              required
            />
          </Grid>
          <Grid item xs={3}>
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
    </Box>
  );
};

export default VerseForm;
