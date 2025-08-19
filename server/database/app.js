'use strict';

const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');

const app = express();
const port = 3030;

// Middlewares
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// Load seed data
const reviewsData = JSON.parse(fs.readFileSync('reviews.json', 'utf8'));
const dealershipsData = JSON.parse(fs.readFileSync('dealerships.json', 'utf8'));

// DB connect
mongoose
  .connect('mongodb://mongo_db:27017/', { dbName: 'dealershipsDB' })
  .then(() => console.log('MongoDB connected'))
  .catch((err) => console.error('MongoDB connection error:', err));

// Models
const Reviews = require('./review');
const Dealerships = require('./dealership');

// Seed (run once on boot; safe with await/try-catch)
(async () => {
  try {
    await Reviews.deleteMany({});
    await Reviews.insertMany(reviewsData.reviews);

    await Dealerships.deleteMany({});
    await Dealerships.insertMany(dealershipsData.dealerships);

    console.log('Database seeded.');
  } catch (error) {
    console.error('Error initializing database:', error);
  }
})();

// Routes
app.get('/', (req, res) => {
  res.send('Welcome to the Mongoose API');
});

// Fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Fetch reviews by dealer id
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const dealerId = Number.isNaN(Number(req.params.id))
      ? req.params.id
      : Number(req.params.id);
    const documents = await Reviews.find({ dealership: dealerId });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Fetch all dealers
app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Fetch dealers by state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const documents = await Dealerships.find({ state: req.params.state });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Fetch single dealer by id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const dealerId = Number.isNaN(Number(req.params.id))
      ? req.params.id
      : Number(req.params.id);
    const documents = await Dealerships.find({ id: dealerId });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Insert review
app.post('/insert_review', async (req, res) => {
  try {
    const data = req.body;

    const last = await Reviews.find().sort({ id: -1 }).limit(1);
    const newId = last.length > 0 ? last[0].id + 1 : 1;

    const review = new Reviews({
      id: newId,
      name: data.name,
      dealership: data.dealership,
      review: data.review,
      purchase: data.purchase,
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: data.car_year,
    });

    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start server
app.listen(port, () => {
  // eslint-disable-next-line no-console
  console.log(`Server is running on http://localhost:${port}`);
});

