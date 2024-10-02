import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Grid } from '@mui/material';

const VerseForm: React.FC = () => {
  const [book, setBook] = useState('');
  const [chapter, setChapter] = useState('');
  const [verse, setVerse] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Check if Book and Chapter are filled
    if (!book || !chapter) {
      alert('Please fill in both Book and Chapter');
      return;
    }

    // Proceed with form submission logic
    console.log(`Book: ${book}, Chapter: ${chapter}, Verse: ${verse || 'All verses'}`);
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: 2,
        maxWidth: 800,
        margin: '0 auto',
      }}
    >
      <Typography variant="h4" gutterBottom>
        Verse Lookup
      </Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          <Grid item xs={4}>
            <TextField
              label="Book"
              value={book}
              onChange={(e) => setBook(e.target.value)}
              fullWidth
              required
            />
          </Grid>
          <Grid item xs={4}>
            <TextField
              label="Chapter"
              value={chapter}
              onChange={(e) => setChapter(e.target.value)}
              fullWidth
              required
            />
          </Grid>
          <Grid item xs={4}>
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
